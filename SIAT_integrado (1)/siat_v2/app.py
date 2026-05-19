# ============================================================
# app.py — SIAT integrado com o banco empresa.db do parceiro
# ============================================================
from flask import Flask
from database.db import db
from models.models import (Admin, Cliente, Empresa, Consulta, Lancamento,
                           Endereco, Cnae, NaturezaJuridica, PorteEmpresa, RegimeTributario)
from routes.auth         import auth_bp
from routes.dashboard    import dashboard_bp
from routes.empresas     import empresas_bp
from routes.clientes     import clientes_bp
from routes.consultas    import consultas_bp
from routes.financeiro   import financeiro_bp
from routes.relatorios   import relatorios_bp
from routes.configuracoes import config_bp
from routes.landing      import landing_bp
import os
from werkzeug.security import generate_password_hash

def create_app():
    app = Flask(__name__)
    app.secret_key = "siat-secret-2025"

    # Aponta para o banco empresa.db do parceiro
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "sqlite:///" + os.path.join(basedir, "database", "empresa.db")
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Registrar blueprints
    app.register_blueprint(landing_bp)
    app.register_blueprint(auth_bp,        url_prefix="/auth")
    app.register_blueprint(dashboard_bp,   url_prefix="/dashboard")
    app.register_blueprint(empresas_bp,    url_prefix="/empresas")
    app.register_blueprint(clientes_bp,    url_prefix="/clientes")
    app.register_blueprint(consultas_bp,   url_prefix="/consultas")
    app.register_blueprint(financeiro_bp,  url_prefix="/financeiro")
    app.register_blueprint(relatorios_bp,  url_prefix="/relatorios")
    app.register_blueprint(config_bp,      url_prefix="/configuracoes")

    with app.app_context():
        # Cria apenas as tabelas que ainda não existem (não apaga o banco do parceiro)
        db.create_all()

        # Admin padrão (só cria se não existir)
        if not Admin.query.filter_by(email="admin@siat.com").first():
            admin = Admin(
                nome="Administrador",
                email="admin@siat.com",
                senha_hash=generate_password_hash("admin123")
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin padrão criado: admin@siat.com / admin123")

        print(f"✅ Banco conectado: empresa.db")
        print(f"   Empresas no banco: {Empresa.query.count()}")
        print(f"   Regimes tributários: {RegimeTributario.query.count()}")

    return app

if __name__ == "__main__":
    app = create_app()
    print("🚀 SIAT rodando em http://localhost:5000")
    app.run(debug=True)
