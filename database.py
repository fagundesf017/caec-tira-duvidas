import sqlite3


def conectar():
    conexao = sqlite3.connect("caec.db")
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_banco():

    conexao = conectar()

    cursor = conexao.cursor()

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
            senha TEXT NOT NULL
        )
    """)

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