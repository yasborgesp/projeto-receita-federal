# 🏛️ SIAT — Sistema Inteligente de Análise Tributária

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white"/>
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white"/>
  <img src="https://img.shields.io/badge/SQLAlchemy-ORM-red?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/BrasilAPI-Receita%20Federal-009b3a?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/HTML%2FCSS%2FJS-Puro-E34F26?style=for-the-badge&logo=html5&logoColor=white"/>
</p>

<p align="center">
  Sistema web completo de consulta e análise tributária voltado para escritórios de contabilidade, com integração em tempo real à Receita Federal do Brasil.
</p>

---

## 📌 Sobre o Projeto

O **SIAT** é um projeto acadêmico desenvolvido para a disciplina de **Desenvolvimento Rápido de Aplicações em Python** no **Centro Universitário UniFatecie — Paranavaí/PR**.

O sistema foi desenvolvido com foco em produtividade e velocidade de entrega, utilizando o microframework **Flask** em conjunto com **SQLAlchemy ORM**, banco de dados **SQLite** e consumo de **API pública da Receita Federal** via BrasilAPI. O frontend foi construído com **HTML5, CSS3 e JavaScript puro**, sem frameworks externos.

O objetivo é simular uma ferramenta real usada por contadores e escritórios contábeis, demonstrando na prática os conceitos de desenvolvimento ágil com Python.

---

## 🎯 Objetivos do Trabalho

- Aplicar os conceitos de **desenvolvimento rápido com Python** usando Flask
- Demonstrar o uso de **ORM com SQLAlchemy** para modelagem e persistência de dados
- Integrar uma **API pública externa** (BrasilAPI / Receita Federal)
- Construir um sistema web **completo e funcional** com múltiplas páginas
- Praticar **boas práticas** de organização de código (blueprints, models, routes)
- Trabalhar com **banco de dados relacional** SQLite com tabelas normalizadas

---

## ✨ Funcionalidades

| Módulo | Descrição |
|---|---|
| 🌐 **Landing Page** | Página pública com apresentação do sistema, planos e formulário de contato |
| 🔐 **Autenticação** | Login seguro com senha criptografada via Werkzeug |
| 📊 **Dashboard** | Painel com métricas gerais, gráficos e consultas recentes |
| 🏢 **Empresas** | Cadastro de empresas e consulta de CNPJ em tempo real via BrasilAPI |
| 👥 **Clientes** | Cadastro e gerenciamento de clientes do escritório |
| 🔍 **Consultas** | Histórico completo de todas as consultas realizadas |
| 💰 **Financeiro** | Controle de receitas, despesas e lançamentos pendentes |
| 📈 **Relatórios** | Indicadores e resumos gerenciais do sistema |
| ⚙️ **Configurações** | Gerenciamento do perfil do administrador |

---

## 🛠️ Tecnologias Utilizadas

### Backend
| Tecnologia | Versão | Uso |
|---|---|---|
| Python | 3.10+ | Linguagem principal |
| Flask | 3.0 | Microframework web |
| SQLAlchemy | 3.1 | ORM para banco de dados |
| Werkzeug | 3.0 | Criptografia de senhas |
| Requests | 2.32 | Consumo de API externa |

### Frontend
| Tecnologia | Uso |
|---|---|
| HTML5 | Estrutura das páginas |
| CSS3 | Estilização e design system |
| JavaScript puro | Interatividade, máscaras e chamadas à API |

### Banco de Dados
| Tecnologia | Uso |
|---|---|
| SQLite | Banco de dados relacional local |
| empresa.db | Arquivo único com todas as tabelas |

### API Externa
| API | Uso |
|---|---|
| BrasilAPI | Consulta de CNPJ direto da Receita Federal |

---

## 📁 Estrutura do Projeto

```
siat/
│
├── app.py                        # Inicialização do Flask e configuração geral
├── requirements.txt              # Dependências do projeto
├── README.md                     # Documentação
├── .gitignore
│
├── database/
│   ├── db.py                     # Instância do SQLAlchemy
│   └── empresa.db                # Banco de dados SQLite
│
├── models/
│   └── models.py                 # Modelos ORM (Empresa, Cliente, Admin...)
│
├── routes/
│   ├── landing.py                # Rota da landing page
│   ├── auth.py                   # Login e logout
│   ├── dashboard.py              # Dashboard principal
│   ├── empresas.py               # CRUD de empresas + consulta CNPJ
│   ├── clientes.py               # CRUD de clientes
│   ├── consultas.py              # Histórico de consultas
│   ├── financeiro.py             # Módulo financeiro
│   ├── relatorios.py             # Relatórios e indicadores
│   └── configuracoes.py          # Configurações da conta
│
├── templates/
│   ├── base.html                 # Layout base com sidebar
│   ├── index.html                # Landing page
│   ├── login.html                # Tela de autenticação
│   ├── dashboard.html            # Dashboard
│   ├── empresas.html             # Página de empresas
│   ├── clientes.html             # Página de clientes
│   ├── consultas.html            # Página de consultas
│   ├── financeiro.html           # Página financeira
│   ├── relatorios.html           # Relatórios
│   └── configuracoes.html        # Configurações
│
└── static/
    ├── css/
    │   └── style.css             # Design system completo
    └── js/
        └── main.js               # JavaScript: máscaras, API, gráficos, modais
```

---

## 🗄️ Modelagem do Banco de Dados

O banco de dados `empresa.db` foi desenvolvido com estrutura normalizada, seguindo os princípios de banco de dados relacionais:

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│    empresa       │────>│    endereco      │     │   natureza_juridica  │
├─────────────────┤     ├──────────────────┤     ├─────────────────────┤
│ id              │     │ id               │     │ id                  │
│ cnpj            │     │ cidade           │     │ classificacao        │
│ razao_social    │     │ rua              │     │ descricao            │
│ nome_fantasia   │     │ numero           │     └─────────────────────┘
│ situacao        │     │ bairro           │
│ capital_social  │     │ uf               │     ┌─────────────────────┐
│ email           │     │ cep              │     │   porte_empresa      │
│ telefone        │     └──────────────────┘     ├─────────────────────┤
│ endereco_id ────┘                               │ id                  │
│ cnae_id         │     ┌──────────────────┐     │ categoria            │
│ natureza_id     │     │      cnae        │     │ faturamento          │
│ porte_id        │     ├──────────────────┤     └─────────────────────┘
│ regime_id       │     │ id               │
└─────────────────┘     │ codigo           │     ┌─────────────────────┐
                         │ descricao        │     │  regime_tributario   │
┌─────────────────┐     └──────────────────┘     ├─────────────────────┤
│     admin       │                               │ id                  │
├─────────────────┤     ┌──────────────────┐     │ tributacao           │
│ id              │     │    clientes      │     │ descricao            │
│ nome            │     ├──────────────────┤     └─────────────────────┘
│ email           │     │ id               │
│ senha_hash      │     │ nome             │     ┌─────────────────────┐
└─────────────────┘     │ email            │     │    lancamentos       │
                         │ telefone         │     ├─────────────────────┤
┌─────────────────┐     │ cpf              │     │ id                  │
│    consultas    │     │ situacao         │     │ descricao            │
├─────────────────┤     └──────────────────┘     │ valor               │
│ id              │                               │ tipo                │
│ tipo            │                               │ status              │
│ documento       │                               │ vencimento          │
│ resultado       │                               └─────────────────────┘
│ razao_social    │
│ data_consulta   │
└─────────────────┘
```

---

## 🌐 Integração com a API

O sistema consome a **BrasilAPI** para consultas de CNPJ em tempo real:

```
GET https://brasilapi.com.br/api/cnpj/v1/{cnpj}
```

**Dados retornados e salvos no banco:**
- Razão social e nome fantasia
- Situação cadastral
- CNAE principal e secundários
- Natureza jurídica e porte
- Endereço completo
- Capital social, telefone e e-mail
- Quadro Societário (QSA)

**Vantagens da BrasilAPI:**
- ✅ Totalmente gratuita
- ✅ Sem necessidade de chave de API
- ✅ Dados oficiais da Receita Federal do Brasil
- ✅ Resposta em formato JSON

---

## 🚀 Como Rodar o Projeto

### Pré-requisitos
- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)
- Git

### Passo a passo

**1. Clone o repositório**
```bash
git clone https://github.com/seu-usuario/siat.git
cd siat
```

**2. Instale as dependências**
```bash
pip install -r requirements.txt
```

**3. Execute a aplicação**
```bash
python app.py
```

**4. Acesse no navegador**
```
http://localhost:5000
```

### Dependências (`requirements.txt`)
```
flask==3.0.3
flask-sqlalchemy==3.1.1
werkzeug==3.0.3
requests==2.32.3
```

---

## 🔐 Acesso ao Sistema

| Campo | Valor padrão |
|---|---|
| E-mail | `admin@siat.com` |
| Senha | `admin123` |

> ⚠️ Recomendamos alterar a senha após o primeiro acesso em **Configurações**.

---

## 📐 Conceitos Aplicados

Este projeto demonstra na prática os seguintes conceitos da disciplina:

- **Flask Blueprints** — organização do código em módulos independentes por funcionalidade
- **SQLAlchemy ORM** — mapeamento objeto-relacional, relacionamentos entre tabelas (ForeignKey, relationship)
- **Jinja2** — sistema de templates com herança (`{% extends %}`), loops e condicionais
- **Flask Sessions** — controle de autenticação e estado do usuário
- **Werkzeug** — hash seguro de senhas com `generate_password_hash` e `check_password_hash`
- **Requests** — consumo de API REST externa com tratamento de erros
- **JavaScript assíncrono** — chamadas `fetch` para consulta de CNPJ sem recarregar a página
- **Design System** — CSS customizado com variáveis, componentes reutilizáveis e responsividade

---

## 📄 Licença

Projeto desenvolvido para fins **acadêmicos** na disciplina de Desenvolvimento Rápido de Aplicações em Python — Centro Universitário UniFatecie, Paranavaí/PR.
