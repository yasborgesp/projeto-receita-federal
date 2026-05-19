# routes/financeiro.py
from flask import Blueprint, render_template, request, redirect, url_for, session
from models.models import Lancamento
from database.db import db
from routes.auth import login_required
from datetime import date

financeiro_bp = Blueprint("financeiro", __name__)

@financeiro_bp.route("/")
@login_required
def index():
    lancamentos = Lancamento.query.order_by(Lancamento.criado_em.desc()).all()
    receitas   = sum(l.valor for l in lancamentos if l.tipo=="Receita")
    despesas   = sum(l.valor for l in lancamentos if l.tipo=="Despesa")
    pendentes  = sum(l.valor for l in lancamentos if l.status=="Pendente")
    return render_template("financeiro.html",
        lancamentos=lancamentos, receitas=receitas,
        despesas=despesas, pendentes=pendentes,
        admin_nome=session.get("admin_nome","Admin"))

@financeiro_bp.route("/cadastrar", methods=["POST"])
@login_required
def cadastrar():
    venc_str = request.form.get("vencimento","")
    venc = None
    if venc_str:
        try: venc = date.fromisoformat(venc_str)
        except: pass
    l = Lancamento(
        descricao=request.form.get("descricao",""),
        valor=float(request.form.get("valor",0) or 0),
        tipo=request.form.get("tipo","Receita"),
        status=request.form.get("status","Pendente"),
        vencimento=venc,
    )
    db.session.add(l); db.session.commit()
    return redirect(url_for("financeiro.index"))

@financeiro_bp.route("/deletar/<int:id>", methods=["POST"])
@login_required
def deletar(id):
    l = Lancamento.query.get_or_404(id)
    db.session.delete(l); db.session.commit()
    return redirect(url_for("financeiro.index"))
