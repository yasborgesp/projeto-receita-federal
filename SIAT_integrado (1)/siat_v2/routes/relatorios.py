# routes/relatorios.py
from flask import Blueprint, render_template, session
from models.models import Empresa, Cliente, Consulta, Lancamento
from routes.auth import login_required

relatorios_bp = Blueprint("relatorios", __name__)

@relatorios_bp.route("/")
@login_required
def index():
    empresas_ativas   = Empresa.query.filter_by(situacao="ATIVA").count()
    empresas_total    = Empresa.query.count()
    consultas_total   = Consulta.query.count()
    clientes_ativos   = Cliente.query.filter_by(situacao="Ativo").count()
    lancamentos       = Lancamento.query.all()
    receitas_total    = sum(l.valor for l in lancamentos if l.tipo=="Receita")
    despesas_total    = sum(l.valor for l in lancamentos if l.tipo=="Despesa")
    return render_template("relatorios.html",
        empresas_ativas=empresas_ativas, empresas_total=empresas_total,
        consultas_total=consultas_total, clientes_ativos=clientes_ativos,
        receitas_total=receitas_total, despesas_total=despesas_total,
        admin_nome=session.get("admin_nome","Admin"))
