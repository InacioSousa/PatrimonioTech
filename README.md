# PatrimônioTech — Sistema de Controle de Patrimônios
> Desenvolvido para **Fama Soluções**

---

## Sobre o Sistema

O **PatrimônioTech** é um sistema web completo para gestão e rastreamento de equipamentos de TI locados, desenvolvido para centralizar o controle de contratos, chamados de manutenção, movimentações e vencimentos em um único lugar — com acesso via navegador, em qualquer dispositivo.

---

## Stack Tecnológica

| Camada | Tecnologia |
|---|---|
| Backend | Python 3 · Flask · SQLAlchemy |
| Banco de dados | PostgreSQL |
| Frontend | HTML5 · CSS3 · JavaScript (Vanilla) |
| Gráficos | Chart.js 4 |
| Relatórios PDF | ReportLab |
| Relatórios Excel | OpenPyXL |
| Agendamento | APScheduler |
| E-mail | smtplib (SMTP/SSL) |
| QR Code | qrcode.js (CDN) |
| Leitura de código de barras | jsQR · QuaggaJS · BarcodeDetector API |

---

## Funcionalidades

### Equipamentos
- Cadastro completo de **Monitores**, **Desktops**, **Notebooks** e **Estabilizadores**
- Campos específicos por tipo (processador, RAM, armazenamento, polegadas, potência VA)
- Campo **PA** (número de ponto de atendimento)
- Paginação de 20 itens por página com filtros por tipo, empresa, localização e busca textual
- Soft delete com reativação automática ao recadastrar patrimônio excluído
- Filtro de alertas: equipamentos a vencer em até 30 dias
- **Ficha PDF individual** por equipamento com dados, chamados e histórico de movimentações
- **Geração de QR Code** com impressão de etiqueta diretamente pelo navegador
- **Importação em massa** via CSV ou XLSX

### Dashboard
- Cards clicáveis com totais por tipo de equipamento, empresas e alertas
- Cards de chamados (total, abertos, fechados) com navegação direta
- **4 gráficos interativos** com quantidades visíveis:
  - Equipamentos por tipo (doughnut)
  - Status de contratos — vencidos, a vencer, ok (doughnut)
  - Chamados por prioridade (barras)
  - Chamados por mês nos últimos 6 meses (linha)
- Tabela de equipamentos mais próximos de vencer, com paginação

### Chamados de Manutenção
- Registro de chamados com número, tipo de equipamento, datas de abertura e solução
- **Prioridade:** Baixa · Média · Alta · Crítica
- **Status detalhado:** Em análise · Aguardando peça · Em reparo · Resolvido
- Busca de equipamento por patrimônio ou PA com dropdown dinâmico
- Comentários e histórico por chamado com data e usuário
- Filtros por tipo, status e prioridade
- Exportação em **Excel** e **PDF** com filtros de período, status e tipo

### Histórico de Movimentações
- Registro automático de toda alteração de localização ou empresa ao editar equipamento
- Filtro por tipo de equipamento
- Exibido também na ficha PDF do equipamento

### Relatórios
- **Excel geral:** 4 abas (Monitores, Desktops, Notebooks, Estabilizadores) com destaque para contratos a vencer
- **PDF geral:** Landscape A4 com tabelas coloridas por status de vencimento
- **PDF de chamados:** Com filtros de período, status e tipo
- **Ficha PDF por equipamento:** Identificação completa + chamados + histórico

### Busca Global
- Campo na topbar que pesquisa em equipamentos, chamados e localizações simultaneamente
- Resultados agrupados por categoria com navegação direta
- Clique em equipamento abre o modal de edição; clique em localização filtra a lista

### Alertas por E-mail
- Configuração de destinatários, dias de antecedência e ativação
- **Scheduler automático às 08:00:** alerta de contratos a vencer ou vencidos
- **Scheduler automático às 08:30:** alerta de chamados abertos há mais de 7 dias
- E-mails em HTML com tabelas coloridas por criticidade
- Envio de teste e disparo manual pela interface

### Leitor QR Code / Código de Barras
- Câmera ao vivo com mira (requer HTTPS)
- Upload de foto ou galeria
- Compatível com QR Code, Code 128, EAN e outros formatos
- Busca manual por código
- Resultado com edição direta ou cadastro imediato se não encontrado

### Usuários e Perfis
- **Admin:** acesso total, incluindo gestão de usuários e log de atividades
- **Técnico:** visualizar, cadastrar e editar (sem excluir)
- **Comum:** somente visualização
- Criação de usuário com envio automático de senha por e-mail
- Redefinição de senha manual ou por geração automática
- Troca de senha obrigatória no primeiro acesso
- Modal "Meu Perfil" para editar nome e e-mail

### Log de Atividades
- Registro de login, edições e comentários com data/hora e usuário
- Paginação de 50 registros por página
- Disponível apenas para perfil admin

### Modo Escuro
- Toggle na topbar com persistência via `localStorage`
- Paleta completa adaptada via variáveis CSS `[data-theme="dark"]`

---

## Instalação

### Pré-requisitos
- Python 3.10+
- PostgreSQL 14+
- pip

### Dependências
```bash
pip install flask flask-sqlalchemy flask-migrate python-dotenv \
            reportlab openpyxl apscheduler psycopg2-binary pillow
```

### Configuração `.env`
```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/patrimonio_db
SECRET_KEY=sua-chave-secreta-aqui

SMTP_HOST=smtp.seuservidor.com
SMTP_PORT=465
SMTP_USER=email@empresa.com
SMTP_PASS=sua-senha-smtp
SMTP_FROM=PatrimônioTech <email@empresa.com>

# Opcional — SSL
SSL_CERT=caminho/para/cert.pem
SSL_KEY=caminho/para/key.pem
```

### Inicialização
```bash
# Cria as tabelas e migra colunas existentes
# Inicia o servidor
python app.py
```

O servidor sobe em `http://0.0.0.0:5000`. Se `SSL_CERT` e `SSL_KEY` estiverem configurados e os arquivos existirem, sobe automaticamente em HTTPS.

### Credenciais padrão
| Campo | Valor |
|---|---|
| E-mail | `admin@patrimonio.local` |
| Senha | `Admin@123` |

> A senha deve ser trocada no primeiro acesso.

---

## Importação em Massa

Acesse **Importar Planilha** na sidebar. O arquivo (CSV ou XLSX) deve conter as colunas:

| Coluna | Obrigatório |
|---|---|
| `tipo` | ✅ Monitor · Desktop · Estabilizador · Notebook |
| `numero_patrimonio` | ✅ |
| `pa` | — |
| `marca` | — |
| `modelo` | — |
| `localizacao` | — |
| `empresa` | — (deve existir no cadastro) |
| `data_aluguel` | — formato `AAAA-MM-DD` |
| `data_fim_fidelidade` | — formato `AAAA-MM-DD` |
| `observacoes` | — |

Patrimônios já existentes são atualizados; novos são criados.

---

## Estrutura de Arquivos

```
patrimonio/
├── app.py                  # Backend completo (Flask + rotas + models)
├── .env                    # Variáveis de ambiente (não versionar)
├── README.md
└── templates/
    ├── index.html          # Interface principal (SPA)
    ├── login.html          # Tela de login
    └── trocar_senha.html   # Troca obrigatória de senha
```

---

## Observações

- O sistema usa **soft delete** — equipamentos excluídos ficam com `ativo=False` e podem ser reativados ao recadastrar o mesmo número de patrimônio
- O leitor de câmera ao vivo exige **HTTPS** — configure SSL ou use `localhost`
- O scheduler de alertas usa o fuso horário `America/Fortaleza`
- Todos os campos de texto são armazenados em **maiúsculas**

---

*PatrimônioTech — Fama Soluções*
