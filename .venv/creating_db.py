import sqlite3
from werkzeug.security import generate_password_hash

# Função para criar o banco de dados e as tabelas
def create_tables():
    # Conectar ao banco de dados (se não existir, será criado)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Criar a tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0
        )
    ''')

    # Criar a tabela de postagens públicas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            author TEXT NOT NULL,
            FOREIGN KEY (author) REFERENCES users (username)
        )
    ''')

    # Criar a tabela de mensagens privadas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS private_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            recipient TEXT NOT NULL,
            author TEXT NOT NULL,
            FOREIGN KEY (author) REFERENCES users (username),
            FOREIGN KEY (recipient) REFERENCES users (username)
        )
    ''')

    # Inserir um usuário administrador padrão (se não existir)
    default_admin_username = 'admin'
    default_admin_password = 'admin_password'
    hashed_password = generate_password_hash(default_admin_password)
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password, is_admin)
        VALUES (?, ?, 1)
    ''', (default_admin_username, hashed_password))

    # Commit e fechar conexão
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
    print('Banco de dados e tabelas criados com sucesso.')
