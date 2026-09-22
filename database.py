import os
import sqlite3

# Verifica se existe um banco PostgreSQL configurado
DATABASE_URL = os.environ.get("DATABASE_URL")


class CursorCompat:
    def __init__(self, cursor, postgres=False):
        self.cursor = cursor
        self.postgres = postgres

    def execute(self, sql, params=None):
        # PostgreSQL usa %s; SQLite usa ?
        if self.postgres:
            sql = sql.replace("?", "%s")

        if params is None:
            return self.cursor.execute(sql)

        return self.cursor.execute(sql, params)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def __getattr__(self, nome):
        return getattr(self.cursor, nome)


class ConexaoCompat:
    def __init__(self, conexao, postgres=False):
        self.conexao = conexao
        self.postgres = postgres

    def cursor(self):
        if self.postgres:
            import psycopg
            from psycopg.rows import dict_row

            cursor = self.conexao.cursor(row_factory=dict_row)
        else:
            cursor = self.conexao.cursor()

        return CursorCompat(cursor, self.postgres)

    def commit(self):
        self.conexao.commit()

    def close(self):
        self.conexao.close()


def conectar():

    # ==============================
    # NEON / POSTGRESQL
    # ==============================

    if DATABASE_URL:
        import psycopg

        conexao = psycopg.connect(DATABASE_URL)

        return ConexaoCompat(
            conexao,
            postgres=True
        )

    # ==============================
    # SQLITE LOCAL
    # ==============================

    conexao = sqlite3.connect("caec.db")
    conexao.row_factory = sqlite3.Row

    return ConexaoCompat(
        conexao,
        postgres=False
    )


def criar_banco():

    conexao = conectar()
    cursor = conexao.cursor()

    if DATABASE_URL:

        # ==============================
        # POSTGRESQL / NEON
        # ==============================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS duvidas (
                id SERIAL PRIMARY KEY,
                disciplina TEXT NOT NULL,
                nome TEXT NOT NULL,
                assunto TEXT NOT NULL,
                duvida TEXT NOT NULL,
                resposta TEXT DEFAULT '',
                nome_resposta TEXT DEFAULT '',
                sim INTEGER DEFAULT 0,
                nao INTEGER DEFAULT 0,
                data_criacao TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                token_recuperacao TEXT,
                expiracao_token TEXT
            )
        """)

    else:

        # ==============================
        # SQLITE LOCAL
        # ==============================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS duvidas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                disciplina TEXT NOT NULL,
                nome TEXT NOT NULL,
                assunto TEXT NOT NULL,
                duvida TEXT NOT NULL,
                resposta TEXT DEFAULT '',
                nome_resposta TEXT DEFAULT '',
                sim INTEGER DEFAULT 0,
                nao INTEGER DEFAULT 0,
                data_criacao TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                token_recuperacao TEXT,
                expiracao_token TEXT
            )
        """)

        # Migração para bancos SQLite antigos
        try:
            cursor.execute("""
                ALTER TABLE usuarios
                ADD COLUMN token_recuperacao TEXT
            """)
        except sqlite3.OperationalError:
            pass

        try:
            cursor.execute("""
                ALTER TABLE usuarios
                ADD COLUMN expiracao_token TEXT
            """)
        except sqlite3.OperationalError:
            pass

    conexao.commit()
    conexao.close()


if __name__ == "__main__":
    criar_banco()
    print("Banco de dados criado com sucesso!")