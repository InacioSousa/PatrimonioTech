"""
Migration completa — adiciona TODAS as colunas novas de uma vez.
Execute: python migrar_tudo.py
"""
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(os.getenv('DATABASE_URL'))
conn.autocommit = True
cur = conn.cursor()

migrations = [
    # Coluna PA em todas as tabelas de equipamento
    ("ALTER TABLE monitores       ADD COLUMN IF NOT EXISTS pa VARCHAR(50);",       "monitores.pa"),
    ("ALTER TABLE desktops        ADD COLUMN IF NOT EXISTS pa VARCHAR(50);",       "desktops.pa"),
    ("ALTER TABLE estabilizadores ADD COLUMN IF NOT EXISTS pa VARCHAR(50);",       "estabilizadores.pa"),
    ("ALTER TABLE notebooks       ADD COLUMN IF NOT EXISTS pa VARCHAR(50);",       "notebooks.pa"),
    # Coluna senha_alterada em usuarios
    ("ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS senha_alterada BOOLEAN DEFAULT TRUE;", "usuarios.senha_alterada"),
]

print("=" * 50)
print("  Migration PatrimônioTech")
print("=" * 50)

for sql, nome in migrations:
    try:
        cur.execute(sql)
        print(f"✅ {nome}")
    except Exception as e:
        print(f"❌ {nome} — {e}")

# Verifica quais colunas existem agora
print("\nVerificando colunas no banco...")
for tabela, coluna in [("monitores","pa"),("desktops","pa"),("estabilizadores","pa"),("notebooks","pa"),("usuarios","senha_alterada")]:
    cur.execute(f"""
        SELECT COUNT(*) FROM information_schema.columns
        WHERE table_name='{tabela}' AND column_name='{coluna}'
    """)
    existe = cur.fetchone()[0] > 0
    print(f"  {'✅' if existe else '❌'} {tabela}.{coluna} {'existe' if existe else 'NÃO EXISTE'}")

cur.close()
conn.close()
print("\nConcluído! Reinicie o servidor: python app.py")


# ── Preenche criado_em nulo nos equipamentos antigos ──────────────────────────
print("\nPreenchendo criado_em nulo nos equipamentos antigos...")
for tabela in ['monitores', 'desktops', 'estabilizadores', 'notebooks']:
    try:
        conn2 = psycopg2.connect(os.getenv('DATABASE_URL'))
        conn2.autocommit = True
        cur2 = conn2.cursor()
        cur2.execute(f"UPDATE {tabela} SET criado_em = NOW() WHERE criado_em IS NULL;")
        print(f"  ✅ {tabela}: {cur2.rowcount} registro(s) atualizado(s)")
        cur2.close(); conn2.close()
    except Exception as e:
        print(f"  ❌ {tabela}: {e}")


# ── Cria tabela config_alerta ─────────────────────────────────────────────────
print("\nCriando tabela config_alerta...")
try:
    conn3 = psycopg2.connect(os.getenv('DATABASE_URL'))
    conn3.autocommit = True
    cur3 = conn3.cursor()
    cur3.execute("""
        CREATE TABLE IF NOT EXISTS config_alerta (
            id           SERIAL PRIMARY KEY,
            emails       TEXT DEFAULT '',
            dias_aviso   INTEGER DEFAULT 10,
            ativo        BOOLEAN DEFAULT TRUE,
            ultimo_envio TIMESTAMP
        );
    """)
    print("  ✅ config_alerta criada/verificada")
    cur3.close(); conn3.close()
except Exception as e:
    print(f"  ❌ config_alerta: {e}")


# ── Cria tabela chamados ───────────────────────────────────────────────────────
print("\nCriando tabela chamados...")
try:
    conn4 = psycopg2.connect(os.getenv('DATABASE_URL'))
    conn4.autocommit = True
    cur4 = conn4.cursor()
    cur4.execute("""
        CREATE TABLE IF NOT EXISTS chamados (
            id                SERIAL PRIMARY KEY,
            numero_chamado    VARCHAR(100) NOT NULL,
            tipo_equipamento  VARCHAR(30) NOT NULL,
            equipamento_id    INTEGER NOT NULL,
            data_abertura     DATE NOT NULL,
            data_solucao      DATE,
            descricao         TEXT,
            solucao           TEXT,
            status            VARCHAR(20) DEFAULT 'aberto',
            criado_em         TIMESTAMP DEFAULT NOW()
        );
    """)
    print("  ✅ chamados criada/verificada")
    cur4.close(); conn4.close()
except Exception as e:
    print(f"  ❌ chamados: {e}")


# ── Cria tabelas novas ────────────────────────────────────────────────────────
print("\nCriando novas tabelas...")
novas = [
    ("movimentacoes", """CREATE TABLE IF NOT EXISTS movimentacoes (
        id               SERIAL PRIMARY KEY,
        tipo_equipamento VARCHAR(30) NOT NULL,
        equipamento_id   INTEGER NOT NULL,
        campo_alterado   VARCHAR(50),
        valor_anterior   TEXT,
        valor_novo       TEXT,
        usuario_id       INTEGER REFERENCES usuarios(id),
        criado_em        TIMESTAMP DEFAULT NOW()
    );"""),
    ("log_atividades", """CREATE TABLE IF NOT EXISTS log_atividades (
        id         SERIAL PRIMARY KEY,
        usuario_id INTEGER REFERENCES usuarios(id),
        acao       VARCHAR(50),
        entidade   VARCHAR(50),
        detalhe    TEXT,
        criado_em  TIMESTAMP DEFAULT NOW()
    );"""),
    ("comentarios_chamado", """CREATE TABLE IF NOT EXISTS comentarios_chamado (
        id         SERIAL PRIMARY KEY,
        chamado_id INTEGER NOT NULL REFERENCES chamados(id) ON DELETE CASCADE,
        usuario_id INTEGER REFERENCES usuarios(id),
        texto      TEXT NOT NULL,
        criado_em  TIMESTAMP DEFAULT NOW()
    );"""),
]
for nome, sql in novas:
    try:
        conn5 = psycopg2.connect(os.getenv('DATABASE_URL'))
        conn5.autocommit = True
        cur5 = conn5.cursor()
        cur5.execute(sql)
        print(f"  ✅ {nome} criada/verificada")
        cur5.close(); conn5.close()
    except Exception as e:
        print(f"  ❌ {nome}: {e}")

# ── Colunas prioridade e status_detalhe em chamados ───────────────────────────
print("\nAdicionando colunas prioridade e status_detalhe em chamados...")
try:
    conn6 = psycopg2.connect(os.getenv('DATABASE_URL'))
    conn6.autocommit = True
    cur6 = conn6.cursor()
    for col, defval, tipo in [
        ("prioridade",     "media",      "VARCHAR(20)"),
        ("status_detalhe", "em_analise", "VARCHAR(30)"),
    ]:
        cur6.execute(f"ALTER TABLE chamados ADD COLUMN IF NOT EXISTS {col} {tipo} DEFAULT '{defval}'")
        print(f"  ✅ {col}")
    cur6.close(); conn6.close()
except Exception as e:
    print(f"  ❌ {e}")