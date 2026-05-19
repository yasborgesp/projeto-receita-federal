# routes/configuracoes.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.models import Admin
from database.db import db
from routes.auth import login_required
from werkzeug.security import generate_password_hash, check_password_hash

config_bp = Blueprint("config", __name__)

@config_bp.route("/")
@login_required
def index():
    admin = Admin.query.get(session["admin_id"])
    return render_template("configuracoes.html", admin=admin,
                           admin_nome=session.get("admin_nome","Admin"))

@config_bp.route("/atualizar", methods=["POST"])
@login_required
def atualizar():
    admin = Admin.query.get(session["admin_id"])
    admin.nome  = request.form.get("nome", admin.nome)
    admin.email = request.form.get("email", admin.email)
    nova_senha  = request.form.get("nova_senha","")
    if nova_senha:
        admin.senha_hash = generate_password_hash(nova_senha)
    db.session.commit()
    session["admin_nome"] = admin.nome
    return redirect(url_for("config.index"))
