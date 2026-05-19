# routes/consultas.py
from flask import Blueprint, render_template, request, jsonify, session
from models.models import Consulta
from database.db import db
from routes.auth import login_required
import requests, re

consultas_bp = Blueprint("consultas", __name__)

@consultas_bp.route("/")
@login_required
def index():
    historico = Consulta.query.order_by(Consulta.data_consulta.desc()).limit(50).all()
    return render_template("consultas.html", historico=historico,
                           admin_nome=session.get("admin_nome","Admin"))

@consultas_bp.route("/cnpj/<cnpj>")
@login_required
def consultar_cnpj(cnpj):
    cnpj_limpo = re.sub(r'\D','',cnpj)
    try:
        r = requests.get(f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}", timeout=10)
        if r.status_code == 200:
            d = r.json()
            c = Consulta(tipo="CNPJ", documento=cnpj_limpo,
                         resultado="Encontrado", razao_social=d.get("razao_social",""))
            db.session.add(c); db.session.commit()
            return jsonify({"ok": True, "data": d})
        if r.status_code == 404:
            c = Consulta(tipo="CNPJ", documento=cnpj_limpo, resultado="Não encontrado")
            db.session.add(c); db.session.commit()
            return jsonify({"ok": False, "erro": "CNPJ não encontrado na Receita Federal."})
        return jsonify({"ok": False, "erro": f"Erro HTTP {r.status_code}"})
    except Exception as e:
        return jsonify({"ok": False, "erro": str(e)})
