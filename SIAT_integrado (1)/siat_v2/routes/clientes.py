# routes/clientes.py
from flask import Blueprint, render_template, request, redirect, url_for, session
from models.models import Cliente
from database.db import db
from routes.auth import login_required

clientes_bp = Blueprint("clientes", __name__)

@clientes_bp.route("/")
@login_required
def index():
    q = request.args.get("q","")
    query = Cliente.query
    if q:
        query = query.filter(Cliente.nome.ilike(f"%{q}%") | Cliente.email.ilike(f"%{q}%"))
    clientes = query.order_by(Cliente.criado_em.desc()).all()
    return render_template("clientes.html", clientes=clientes, q=q,
                           admin_nome=session.get("admin_nome","Admin"))

@clientes_bp.route("/cadastrar", methods=["POST"])
@login_required
def cadastrar():
    c = Cliente(
        nome=request.form.get("nome",""),
        email=request.form.get("email",""),
        telefone=request.form.get("telefone",""),
        cpf=request.form.get("cpf",""),
        situacao=request.form.get("situacao","Ativo"),
    )
    db.session.add(c); db.session.commit()
    return redirect(url_for("clientes.index"))

@clientes_bp.route("/deletar/<int:id>", methods=["POST"])
@login_required
def deletar(id):
    c = Cliente.query.get_or_404(id)
    db.session.delete(c); db.session.commit()
    return redirect(url_for("clientes.index"))
