# routes/auth.py — Autenticação
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from models.models import Admin

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email","").strip()
        senha = request.form.get("senha","")
        admin = Admin.query.filter_by(email=email).first()
        if admin and check_password_hash(admin.senha_hash, senha):
            session["admin_id"]   = admin.id
            session["admin_nome"] = admin.nome
            return redirect(url_for("dashboard.index"))
        flash("E-mail ou senha incorretos.", "error")
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if "admin_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated
