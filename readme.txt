# Mercado Preso 🛒

Projeto acadêmico desenvolvido para a disciplina de Desenvolvimento Web no IFBA - Campus Euclides da Cunha. 
Uma plataforma de e-commerce com temática humorística e irônica.

## 🚀 Tecnologias Utilizadas

- **Backend:** Python 3.x, Flask
- **Frontend:** HTML5, CSS3, JavaScript
- **Database:** SQLite com SQLAlchemy ORM
- **Autenticação:** Flask-Login
- **Migrações:** Flask-Migrate
- **Upload de Arquivos:** Flask-Uploads
- **Formulários:** Flask-WTF

## 📦 Funcionalidades

- ✅ Sistema de autenticação de usuários (Vendedores/Compradores)
- ✅ Cadastro e gerenciamento de produtos
- ✅ Sistema de compras virtual
- ✅ Upload de imagens para produtos
- ✅ Interface responsiva
- ✅ Dashboard para vendedores
- ✅ Formulários seguros com Flask-WTF e CSRF protection

## 👥 Desenvolvedores

- Gabriel Lopes
- Ariel Leite
- Eduardo Silva

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git

## 🛠️ Instalação e Configuração

### 1. Clone o repositório
git clone https://github.com/gabrieldonlopes/mercado-preso
cd app

### 2. Crie um ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows

### 3. Instale as dependências
pip install -r requirements.txt

### 4. Configuração do Banco de Dados

#### Opção A: Usar banco pré-populado (mais fácil)
Apenas execute a aplicação - já existe um banco com dados de teste
flask run

#### Opção B: Inicializar com Flask-Migrate (para desenvolvimento)
Remova o banco existente e imagens de upload

rm mercado_preso.db
rm -rf uploads/produtos/*

Inicialize o sistema de migração

flask db init
flask db migrate -m "Initial migration"
flask db upgrade

Execute a aplicação

flask run

## 👤 Usuários de Teste

### Vendedores:
- **Usuário:** gabriel | **Senha:** bonito-pra-dedeu
- **Usuário:** ariel | **Senha:** cara-de-pastel  
- **Usuário:** dudao | **Senha:** cada-de-mamao

## 5. Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
FLASK_APP=.:create_app
FLASK_ENV=development
SECRET_KEY=java_e_muito_melhor

## Executar:
flask run
ou
python app.py

## ⚠️ Notas Importantes

- **Database pré-populada:** Uma database personalizada com dados fictícios está incluída em `mercado_preso.db`. Para testar a aplicação sem ela, recomenda-se usar o Flask-Migrate.

- **Uploads de imagens:** Para inicializar com `flask db` é necessário apagar as imagens em `uploads/produtos/`

- **Flask-WTF:** Todos os formulários utilizam Flask-WTF para validação e proteção CSRF. Certifique-se de que a chave secreta está configurada corretamente no app.

## 🔒 Configuração de Segurança

O projeto utiliza Flask-WTF para:
- Validação de formulários no backend
- Proteção contra CSRF (Cross-Site Request Forgery)
- Campos seguros com WTForms
- Geração automática de tokens CSRF

Certifique-se de definir uma chave secreta segura no arquivo de configuração: