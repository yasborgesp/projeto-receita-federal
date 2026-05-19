# routes/dashboard.py
from flask import Blueprint, render_template, session, redirect, url_for
from models.models import Empresa, Cliente, Consulta, Lancamento
from routes.auth import login_required

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
@login_required
def index():
    total_empresas   = Empresa.query.count()
    total_clientes   = Cliente.query.count()
    total_consultas  = Consulta.query.count()
    empresas_ativas  = Empresa.query.filter_by(situacao="ATIVA").count()
    recentes         = Consulta.query.order_by(Consulta.data_consulta.desc()).limit(8).all()
    return render_template("dashboard.html",
        total_empresas=total_empresas,
        total_clientes=total_clientes,
        total_consultas=total_consultas,
        empresas_ativas=empresas_ativas,
        recentes=recentes,
        admin_nome=session.get("admin_nome","Admin")
    )
