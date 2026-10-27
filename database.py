
import sqlite3

DATABASE = "drivefin.db"

def conectar():
    return sqlite3.connect(DATABASE)

def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lancamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            tipo TEXT NOT NULL
                CHECK(tipo IN ('receita', 'despesa')),
            valor REAL NOT NULL CHECK(valor > 0),
            data TEXT NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()

if __name__ == "__main__":
    criar_tabelas()
    print("Banco de dados DriveFin configurado!")
