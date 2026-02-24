# Access Control & Audit System

Sistema de gerenciamento de acesso e auditoria, desenvolvido em **Python** com **FastAPI**. Permite autenticação de usuários, controle de permissões, gerenciamento de roles e monitoramento de ações.

---

## Funcionalidades

- **Login/Logout** de usuários
- **Gerenciamento de Usuários**: criação, atualização e exclusão
- **Gerenciamento de Roles**: definição de permissões e funções
- **Auditoria**: registro das ações do sistema
- **Dashboard** com interface web responsiva

---

## Tecnologias Utilizadas

- **Backend:** Python, FastAPI  
- **Banco de Dados:** SQLite (pode ser adaptado para MySQL/PostgreSQL)  
- **Autenticação:** Passlib (bcrypt)  
- **Templates:** Jinja2  
- **Front-end:** HTML, CSS  

---

## Estrutura do Projeto

access_control_system/
│
├── src/
│ ├── routers/ # Rotas do sistema (auth, users, roles, audit)
│ ├── models/ # Modelos de banco de dados
│ ├── database/ # Conexão e sessão com banco
│ ├── templates/ # Arquivos HTML
│ └── static/ # CSS e assets
│
├── venv/ # Virtual environment (ignorado pelo git)
├── main.py # Arquivo principal da aplicação
├── README.md # Este arquivo
└── requirements.txt # Dependências Python


---

## Como Rodar o Projeto

1. Clonar o repositório:
```bash
git clone https://github.com/SEU_USUARIO/access_control_system.git
cd access_control_system

2.Criar e ativar o ambiente virtual:

python -m venv venv
# Windows
.\venv\Scripts\Activate.ps1
# Linux/macOS
source venv/bin/activate

3.Instalar dependências:

pip install -r requirements.txt

4.Rodar a aplicação:

python -m uvicorn src.main:app --reload

5.Acessar no navegador:

http://127.0.0.1:800

*Usuário de Teste

Usuário: admin

Senha: 123 (senha criptografada usando bcrypt)

Observações

O projeto já possui templates HTML estilizados para login e dashboard.

O sistema ainda pode ser expandido com CRUD completo de usuários, roles e auditoria.

Recomenda-se não subir a pasta venv para o GitHub.
