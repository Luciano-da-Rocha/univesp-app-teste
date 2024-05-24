import sqlite3

def create_private_posts_table():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()

    # Cria a tabela private_posts se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS private_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            recipient TEXT NOT NULL,
            author TEXT NOT NULL,
            FOREIGN KEY (recipient) REFERENCES users(username),
            FOREIGN KEY (author) REFERENCES users(username)
        )
    ''')

    db.commit()
    db.close()

if __name__ == '__main__':
    create_private_posts_table()
