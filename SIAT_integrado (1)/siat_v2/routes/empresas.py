# routes/empresas.py — integrado com banco do parceiro (tabelas normalizadas)
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from models.models import Empresa, Endereco, Cnae, NaturezaJuridica, PorteEmpresa, RegimeTributario, Consulta
from database.db import db
from routes.auth import login_required
import requests, re

empresas_bp = Blueprint("empresas", __name__)

def limpar_cnpj(cnpj): return re.sub(r'\D', '', cnpj)

@empresas_bp.route("/")
@login_required
def index():
    q = request.args.get("q", "")
    query = Empresa.query
    if q:
        query = query.filter(
            Empresa.razao_social.ilike(f"%{q}%") |
            Empresa.cnpj.ilike(f"%{q}%")
        )
    empresas = query.order_by(Empresa.id.desc()).all()
    regimes  = RegimeTributario.query.all()
    return render_template("empresas.html", empresas=empresas, q=q,
                           regimes=regimes,
                           admin_nome=session.get("admin_nome", "Admin"))

@empresas_bp.route("/cadastrar", methods=["POST"])
@login_required
def cadastrar():
    cnpj = limpar_cnpj(request.form.get("cnpj", ""))
    if Empresa.query.filter_by(cnpj=cnpj).first():
        return redirect(url_for("empresas.index"))

    # Criar endereço
    end = Endereco(
        cidade=request.form.get("cidade", ""),
        rua=request.form.get("rua", ""),
        numero=request.form.get("numero", ""),
        bairro=request.form.get("bairro", ""),
    )
    db.session.add(end)
    db.session.flush()

    # Buscar ou criar CNAE
    cnae_cod = request.form.get("cnae", "")
    cnae = Cnae.query.filter_by(codigo=cnae_cod).first()
    if not cnae and cnae_cod:
        cnae = Cnae(codigo=cnae_cod, descricao="")
        db.session.add(cnae); db.session.flush()

    # Natureza jurídica
    nat_id = request.form.get("natureza_juridica_id")
    nat = NaturezaJuridica.query.get(nat_id) if nat_id else None

    # Porte
    porte_id = request.form.get("porte_empresa_id")
    porte = PorteEmpresa.query.get(porte_id) if porte_id else None

    # Regime tributário
    regime_id = request.form.get("regime_tributario_id")
    regime = RegimeTributario.query.get(regime_id) if regime_id else None

    emp = Empresa(
        cnpj=cnpj,
        razao_social=request.form.get("razao_social", ""),
        nome_fantasia=request.form.get("nome_fantasia", ""),
        situacao=request.form.get("situacao", "ATIVA"),
        endereco_id=end.id,
        cnae_id=cnae.id if cnae else None,
        natureza_juridica_id=nat.id if nat else None,
        porte_empresa_id=porte.id if porte else None,
        regime_tributario_id=regime.id if regime else None,
    )
    db.session.add(emp)
    db.session.commit()
    return redirect(url_for("empresas.index"))

@empresas_bp.route("/deletar/<int:id>", methods=["POST"])
@login_required
def deletar(id):
    emp = Empresa.query.get_or_404(id)
    db.session.delete(emp)
    db.session.commit()
    return redirect(url_for("empresas.index"))

@empresas_bp.route("/buscar-cnpj/<cnpj>")
@login_required
def buscar_cnpj(cnpj):
    """Consulta BrasilAPI e salva usando a estrutura normalizada do parceiro"""
    cnpj_limpo = limpar_cnpj(cnpj)
    try:
        r = requests.get(f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}", timeout=10)
        if r.status_code != 200:
            msg = "CNPJ não encontrado." if r.status_code == 404 else f"Erro {r.status_code}"
            return jsonify({"ok": False, "erro": msg})

        d = r.json()

        # Criar/atualizar Endereco
        end = Endereco(
            cidade=d.get("municipio", ""),
            rua=f"{d.get('tipo_logradouro','')} {d.get('logradouro','')}".strip(),
            numero=d.get("numero", ""),
            bairro=d.get("bairro", ""),
            uf=d.get("uf", ""),
            cep=d.get("cep", ""),
            complemento=d.get("complemento", ""),
        )
        db.session.add(end); db.session.flush()

        # Criar/buscar CNAE
        cnae_cod = str(d.get("cnae_fiscal", ""))
        cnae = Cnae.query.filter_by(codigo=cnae_cod).first()
        if not cnae:
            cnae = Cnae(codigo=cnae_cod, descricao=d.get("cnae_fiscal_descricao", ""))
            db.session.add(cnae); db.session.flush()

        # Criar/buscar Natureza Jurídica
        nat_desc = d.get("descricao_natureza_juridica", "")
        nat = NaturezaJuridica.query.filter_by(classificacao=nat_desc).first()
        if not nat:
            nat = NaturezaJuridica(classificacao=nat_desc, descricao=nat_desc)
            db.session.add(nat); db.session.flush()

        # Criar/buscar Porte
        porte_desc = d.get("descricao_porte", "")
        porte = PorteEmpresa.query.filter_by(categoria=porte_desc).first()
        if not porte:
            porte = PorteEmpresa(categoria=porte_desc, faturamento="—")
            db.session.add(porte); db.session.flush()

        # Salvar/atualizar Empresa
        emp = Empresa.query.filter_by(cnpj=cnpj_limpo).first()
        if not emp:
            emp = Empresa(cnpj=cnpj_limpo)
            db.session.add(emp)

        emp.razao_social         = d.get("razao_social", "")
        emp.nome_fantasia        = d.get("nome_fantasia", "")
        emp.data_abertura        = (d.get("data_inicio_atividade") or "")[:10]
        emp.situacao             = d.get("descricao_situacao_cadastral", "")
        emp.capital_social       = float(d.get("capital_social") or 0)
        emp.email                = d.get("email", "")
        emp.telefone             = d.get("ddd_telefone_1", "")
        emp.municipio            = d.get("municipio", "")
        emp.uf                   = d.get("uf", "")
        emp.endereco_id          = end.id
        emp.cnae_id              = cnae.id
        emp.natureza_juridica_id = nat.id
        emp.porte_empresa_id     = porte.id

        db.session.commit()

        # Registrar consulta no histórico
        c = Consulta(tipo="CNPJ", documento=cnpj_limpo,
                     resultado="Encontrado", razao_social=emp.razao_social)
        db.session.add(c); db.session.commit()

        return jsonify({"ok": True, "data": d})

    except Exception as e:
        db.session.rollback()
        return jsonify({"ok": False, "erro": str(e)})
