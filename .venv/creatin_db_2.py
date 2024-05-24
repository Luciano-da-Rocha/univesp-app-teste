import sqlite3

# Função para conectar ao banco de dados SQLite
def connect_db():
    return sqlite3.connect('database.db')

# Criar tabelas no banco de dados
def create_tables():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        is_admin INTEGER DEFAULT 0
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS posts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT NOT NULL,
                        author TEXT NOT NULL
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS private_posts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT NOT NULL,
                        recipient TEXT NOT NULL,
                        author TEXT NOT NULL
                    )''')
    db.commit()
    db.close()

# Inserir usuário administrador padrão (se não existir)
def insert_default_admin():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        hashed_password = generate_password_hash('admin_password')
        cursor.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)", ('admin', hashed_password, 1))
        db.commit()
    db.close()

if __name__ == '__main__':
    create_tables()
    insert_default_admin()
    print("Banco de dados configurado com sucesso.")
