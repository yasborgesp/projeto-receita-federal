<h1 align="center">
  🏛️ SIAT — Sistema Inteligente de Análise Tributária
</h1>

<p align="center">
  Sistema web completo para escritórios de contabilidade com integração à Receita Federal
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white"/>
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white"/>
  <img src="https://img.shields.io/badge/HTML%2FCSS%2FJS-puro-E34F26?style=for-the-badge&logo=html5&logoColor=white"/>
  <img src="https://img.shields.io/badge/BrasilAPI-Receita%20Federal-009b3a?style=for-the-badge"/>
</p>

---

## 📋 Sobre o Projeto

O **SIAT** é um sistema web desenvolvido como projeto acadêmico no **Centro Universitário UniFatecie**, voltado para contadores e escritórios contábeis. A plataforma permite consultar dados cadastrais de empresas diretamente da Receita Federal, gerenciar clientes, controlar lançamentos financeiros e visualizar relatórios gerenciais em um dashboard moderno.

---

## ✨ Funcionalidades

| Módulo | Descrição |
|---|---|
| 🌐 **Landing Page** | Página inicial com planos, sobre nós e formulário de contato |
| 🔐 **Autenticação** | Login seguro com senha criptografada (Werkzeug) |
| 📊 **Dashboard** | Métricas, gráficos e consultas recentes |
| 🏢 **Empresas** | Cadastro e consulta de CNPJ em tempo real via BrasilAPI |
| 👥 **Clientes** | Cadastro e gerenciamento de clientes do escritório |
| 🔍 **Consultas** | Histórico completo de todas as consultas realizadas |
| 💰 **Financeiro** | Controle de receitas, despesas e pendências |
| 📈 **Relatórios** | Indicadores e resumos do sistema |
| ⚙️ **Configurações** | Gerenciamento da conta de administrador |

---

## 🛠️ Tecnologias

**Backend**
- Python 3.10+
- Flask 3.0
- SQLAlchemy (ORM)
- Werkzeug (segurança de senha)

**Frontend**
- HTML5
- CSS3
- JavaScript puro (sem frameworks)

**Banco de dados**
- SQLite (`empresa.db`)

**API externa**
- [BrasilAPI](https://brasilapi.com.br) — consulta de CNPJ da Receita Federal (gratuita, sem chave)

---

## 📁 Estrutura do Projeto

```
siat/
├── app.py                    # Ponto de entrada da aplicação Flask
├── requirements.txt          # Dependências do projeto
├── README.md
│
├── database/
│   ├── db.py                 # Instância do SQLAlchemy
│   └── empresa.db            # Banco de dados SQLite
│
├── models/
│   └── models.py             # Modelos ORM: Empresa, Cliente, Consulta...
│
├── routes/
│   ├── auth.py               # Login e logout
│   ├── dashboard.py          # Dashboard principal
│   ├── empresas.py           # Gestão de empresas + consulta CNPJ
│   ├── clientes.py           # Gestão de clientes
│   ├── consultas.py          # Histórico de consultas
│   ├── financeiro.py         # Módulo financeiro
│   ├── relatorios.py         # Relatórios
│   ├── configuracoes.py      # Configurações da conta
│   └── landing.py            # Landing page
│
├── templates/
│   ├── base.html             # Layout base com sidebar
│   ├── index.html            # Landing page
│   ├── login.html            # Tela de autenticação
│   ├── dashboard.html
│   ├── empresas.html
│   ├── clientes.html
│   ├── consultas.html
│   ├── financeiro.html
│   ├── relatorios.html
│   └── configuracoes.html
│
└── static/
    ├── css/style.css         # Design system completo
    └── js/main.js            # Máscaras, consultas API, gráficos
```

---

## 🚀 Como Rodar o Projeto

### Pré-requisitos
- Python 3.10 ou superior instalado
- Git instalado

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/siat.git
cd siat
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Execute a aplicação

```bash
python app.py
```

### 4. Acesse no navegador

```
http://localhost:5000
```

---

## 🔐 Acesso Padrão

| Campo | Valor |
|---|---|
| E-mail | `admin@siat.com` |
| Senha | `admin123` |

> ⚠️ Altere a senha padrão após o primeiro acesso em **Configurações**.

---

## 🗄️ Banco de Dados

O sistema utiliza o banco `empresa.db` (SQLite) com as seguintes tabelas:

| Tabela | Descrição |
|---|---|
| `empresa` | Empresas consultadas e cadastradas |
| `endereco` | Endereços das empresas |
| `cnae` | Atividades econômicas |
| `natureza_juridica` | Natureza jurídica das empresas |
| `porte_empresa` | Porte (ME, EPP, etc.) |
| `regime_tributario` | Simples Nacional, Lucro Real, etc. |
| `admin` | Administradores do sistema |
| `clientes` | Clientes do escritório |
| `consultas` | Histórico de consultas realizadas |
| `lancamentos` | Lançamentos financeiros |

---

## 🌐 Integração com a API

O sistema consome a **BrasilAPI** para consultas de CNPJ:

```
GET https://brasilapi.com.br/api/cnpj/v1/{cnpj}
```

- ✅ Gratuita
- ✅ Sem necessidade de chave de API
- ✅ Dados direto da Receita Federal do Brasil

---

## 👨‍💻 Autores

Desenvolvido por estudantes do **Centro Universitário UniFatecie — Paranavaí/PR**

---

## 📄 Licença

Este projeto foi desenvolvido para fins **acadêmicos**.
