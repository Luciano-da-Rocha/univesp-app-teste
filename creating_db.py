import sqlite3

# Função para criar o banco de dados e a tabela de usuários
def create_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY,
            content TEXT NOT NULL,
            author TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def connect_db():
    return sqlite3.connect('database.db')
def add_admin_column():
    db = connect_db()
    cursor = db.cursor()
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0")
        db.commit()
        print("Coluna 'is_admin' adicionada à tabela 'users' com sucesso.")
    except sqlite3.OperationalError as e:
        print("Erro ao adicionar coluna 'is_admin' à tabela 'users':", e)
    finally:
        db.close()
if __name__ == "__main__":
    create_database()
    add_admin_column()
    print("Banco de dados e tabela de usuários criados com sucesso.")
