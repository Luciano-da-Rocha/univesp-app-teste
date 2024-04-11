import sqlite3
from werkzeug.security import generate_password_hash

# Função para conectar ao banco de dados SQLite
def connect_db():
    return sqlite3.connect('database.db')

# Função para adicionar um usuário administrador
def add_admin_user():
    # Dados do usuário administrador
    username = 'admin'
    password = 'administrador'
    hashed_password = generate_password_hash(password)

    # Conectar ao banco de dados
    db = connect_db()
    cursor = db.cursor()

    # Verificar se o usuário já existe
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        print("Usuário 'admin' já existe no banco de dados.")
        return

    # Inserir usuário administrador no banco de dados
    cursor.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)", (username, hashed_password, 1))
    db.commit()
    print("Usuário 'admin' adicionado como administrador.")

    db.close()

if __name__ == '__main__':
    add_admin_user()