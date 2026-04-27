# 🖥 PatrimônioTech — Sistema de Controle de Patrimônios

Sistema web para controle de equipamentos de TI (monitores e desktops) com suporte a leitura de QR code / código de barras, relatórios em PDF e Excel.

---

## ⚙ Pré-requisitos

- Python 3.10+
- PostgreSQL 14+
- pip

---

## 🚀 Instalação passo a passo

### 1. Clone / copie o projeto
```bash
cd patrimonio
```

### 2. Crie o ambiente virtual
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

> Se usar Linux e tiver problema com pyzbar:
> ```bash
> sudo apt-get install libzbar0
> ```

### 4. Configure o banco de dados PostgreSQL

Crie o banco no PostgreSQL:
```sql
CREATE DATABASE patrimonio_db;
CREATE USER patrimonio_user WITH PASSWORD 'sua_senha';
GRANT ALL PRIVILEGES ON DATABASE patrimonio_db TO patrimonio_user;
```

### 5. Configure as variáveis de ambiente

Copie o arquivo de exemplo:
```bash
cp .env.example .env
```

Edite o `.env` com suas configurações:
```
DATABASE_URL=postgresql://patrimonio_user:sua_senha@localhost:5432/patrimonio_db
SECRET_KEY=coloque-uma-chave-aleatoria-e-longa-aqui
FLASK_ENV=development
```

### 6. Crie as tabelas no banco
```bash
python app.py
```
Ou usando Flask-Migrate:
```bash
flask db init
flask db migrate -m "inicial"
flask db upgrade
```

### 7. Execute o servidor
```bash
python app.py
```

Acesse: **http://localhost:5000**

---

## 📁 Estrutura do projeto

```
patrimonio/
├── app.py              # Configuração Flask + banco
├── models.py           # Modelos do banco (Monitor, Desktop, Empresa)
├── routes.py           # Rotas da API e relatórios
├── requirements.txt    # Dependências Python
├── .env.example        # Variáveis de ambiente (modelo)
└── templates/
    └── index.html      # Interface web completa
```

---

## 🔧 Funcionalidades

| Funcionalidade | Descrição |
|---|---|
| Cadastro de monitores | Com patrimônio, marca, polegadas, localização, datas |
| Cadastro de desktops | Com processador, RAM, armazenamento, localização, datas |
| Edição / exclusão | Soft delete (não apaga do banco, só desativa) |
| Leitor QR / barras | Via câmera do dispositivo (web) |
| Busca manual | Por código de patrimônio |
| Empresas locadoras | CRUD completo |
| Relatório Excel | Download com destaque para contratos vencendo |
| Relatório PDF | Relatório formatado com alertas de vencimento |
| Alertas automáticos | Badge de dias restantes para fim de fidelidade |
| Busca e filtros | Por nome, localização, modelo e empresa |

---

## 🌐 API REST

| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/equipamentos` | Lista todos (aceita ?tipo=monitor/desktop&busca=&empresa_id=) |
| GET | `/api/patrimonio/:codigo` | Busca por número de patrimônio |
| POST | `/api/monitores` | Criar monitor |
| PUT | `/api/monitores/:id` | Atualizar monitor |
| DELETE | `/api/monitores/:id` | Desativar monitor |
| POST | `/api/desktops` | Criar desktop |
| PUT | `/api/desktops/:id` | Atualizar desktop |
| DELETE | `/api/desktops/:id` | Desativar desktop |
| GET | `/api/empresas` | Listar empresas |
| POST | `/api/empresas` | Criar empresa |
| GET | `/relatorio/excel` | Download Excel |
| GET | `/relatorio/pdf` | Download PDF |

---

## 🖥 Produção (deploy)

Para rodar em produção use Gunicorn + Nginx:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

---

## 📦 Tecnologias utilizadas

- **Flask** — framework web
- **PostgreSQL + SQLAlchemy** — banco de dados
- **openpyxl** — geração de Excel
- **ReportLab** — geração de PDF
- **html5-qrcode** — leitura de QR/barras pelo navegador
- **IBM Plex Sans / Mono** — tipografia
