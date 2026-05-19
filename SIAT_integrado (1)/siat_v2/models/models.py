# models/models.py
# Modelos que espelham exatamente o banco empresa.db do parceiro de projeto
# + tabelas novas que o SIAT precisa (admin, clientes, consultas, lancamentos)

from database.db import db
from datetime import datetime

# ── Tabelas existentes no banco do parceiro ──────────────────────────────────

class Endereco(db.Model):
    """Endereços das empresas — tabela original do parceiro"""
    __tablename__ = "endereco"
    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cidade      = db.Column(db.String(100))
    rua         = db.Column(db.String(150))
    numero      = db.Column(db.String(20))
    bairro      = db.Column(db.String(100))
    uf          = db.Column(db.String(2))
    cep         = db.Column(db.String(9))
    complemento = db.Column(db.String(100))

class Cnae(db.Model):
    """Atividade econômica — tabela original do parceiro"""
    __tablename__ = "cnae"
    id        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo    = db.Column(db.String(20))
    descricao = db.Column(db.String(255))

class NaturezaJuridica(db.Model):
    """Natureza jurídica — tabela original do parceiro"""
    __tablename__ = "natureza_juridica"
    id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
    classificacao = db.Column(db.String(100))
    descricao     = db.Column(db.String(255))

class PorteEmpresa(db.Model):
    """Porte da empresa — tabela original do parceiro"""
    __tablename__ = "porte_empresa"
    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    categoria   = db.Column(db.String(100))
    faturamento = db.Column(db.String(100))

class RegimeTributario(db.Model):
    """Regime tributário — tabela original do parceiro"""
    __tablename__ = "regime_tributario"
    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tributacao = db.Column(db.String(100))
    descricao  = db.Column(db.String(255))

class Empresa(db.Model):
    """
    Empresas — tabela original do parceiro, com colunas extras adicionadas
    para integração com a BrasilAPI (situacao, capital_social, email, etc.)
    """
    __tablename__ = "empresa"
    id                   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cnpj                 = db.Column(db.String(18), unique=True)
    razao_social         = db.Column(db.String(255))
    nome_fantasia        = db.Column(db.String(255))
    data_abertura        = db.Column(db.String(10))
    # FKs para as tabelas do parceiro
    endereco_id          = db.Column(db.Integer, db.ForeignKey("endereco.id"))
    natureza_juridica_id = db.Column(db.Integer, db.ForeignKey("natureza_juridica.id"))
    porte_empresa_id     = db.Column(db.Integer, db.ForeignKey("porte_empresa.id"))
    regime_tributario_id = db.Column(db.Integer, db.ForeignKey("regime_tributario.id"))
    cnae_id              = db.Column(db.Integer, db.ForeignKey("cnae.id"))
    # Colunas extras adicionadas para integração com BrasilAPI
    situacao             = db.Column(db.String(50))
    capital_social       = db.Column(db.Float)
    email                = db.Column(db.String(200))
    telefone             = db.Column(db.String(30))
    municipio            = db.Column(db.String(100))
    uf                   = db.Column(db.String(2))
    # Relacionamentos
    endereco          = db.relationship("Endereco",          lazy="joined")
    natureza_juridica = db.relationship("NaturezaJuridica",  lazy="joined")
    porte_empresa     = db.relationship("PorteEmpresa",      lazy="joined")
    regime_tributario = db.relationship("RegimeTributario",  lazy="joined")
    cnae              = db.relationship("Cnae",              lazy="joined")

    @property
    def cnpj_formatado(self):
        d = (self.cnpj or "").replace(".", "").replace("/", "").replace("-", "")
        if len(d) == 14:
            return f"{d[:2]}.{d[2:5]}.{d[5:8]}/{d[8:12]}-{d[12:]}"
        return self.cnpj or ""

    @property
    def criado_em(self):
        """Compatibilidade com templates que usam criado_em"""
        return None

# ── Tabelas novas do SIAT ─────────────────────────────────────────────────────

class Admin(db.Model):
    """Administrador do sistema"""
    __tablename__ = "admin"
    id         = db.Column(db.Integer, primary_key=True)
    nome       = db.Column(db.String(120), nullable=False)
    email      = db.Column(db.String(200), unique=True, nullable=False)
    senha_hash = db.Column(db.String(256), nullable=False)
    criado_em  = db.Column(db.DateTime, default=datetime.utcnow)

class Cliente(db.Model):
    """Clientes do escritório contábil"""
    __tablename__ = "clientes"
    id        = db.Column(db.Integer, primary_key=True)
    nome      = db.Column(db.String(200), nullable=False)
    email     = db.Column(db.String(200))
    telefone  = db.Column(db.String(20))
    cpf       = db.Column(db.String(14))
    situacao  = db.Column(db.String(20), default="Ativo")
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

class Consulta(db.Model):
    """Histórico de consultas realizadas"""
    __tablename__ = "consultas"
    id            = db.Column(db.Integer, primary_key=True)
    tipo          = db.Column(db.String(10))
    documento     = db.Column(db.String(20))
    resultado     = db.Column(db.String(50))
    razao_social  = db.Column(db.String(255))
    data_consulta = db.Column(db.DateTime, default=datetime.utcnow)

class Lancamento(db.Model):
    """Lançamentos financeiros"""
    __tablename__ = "lancamentos"
    id         = db.Column(db.Integer, primary_key=True)
    descricao  = db.Column(db.String(200))
    valor      = db.Column(db.Float, default=0)
    tipo       = db.Column(db.String(10))
    status     = db.Column(db.String(20), default="Pendente")
    vencimento = db.Column(db.Date)
    criado_em  = db.Column(db.DateTime, default=datetime.utcnow)
