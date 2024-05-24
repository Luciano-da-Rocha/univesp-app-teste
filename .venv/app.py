from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Função para conectar ao banco de dados SQLite
def connect_db():
    return sqlite3.connect('database.db')

# Rota para a página inicial (mural)
@app.route('/')
def index():
    if 'username' in session:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM posts ORDER BY id DESC")
        posts = cursor.fetchall()

        # Verifica se o usuário é um administrador
        cursor.execute("SELECT is_admin FROM users WHERE username = ?", (session['username'],))
        is_admin = cursor.fetchone()[0]

        db.close()
        return render_template('index.html', username=session['username'], posts=posts, is_admin=is_admin)
    return redirect(url_for('login'))

# Rota para postar uma mensagem
@app.route('/post', methods=['POST'])
def post():
    if 'username' in session:
        content = request.form['content']
        author = session['username']
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO posts (content, author) VALUES (?, ?)", (content, author))
        db.commit()
        db.close()
        flash('Postagem realizada com sucesso!', 'success')
    return redirect(url_for('index'))

# Rota para apagar uma postagem
@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    if 'username' in session:
        db = connect_db()
        cursor = db.cursor()

        # Verifica se o usuário é um administrador
        cursor.execute("SELECT is_admin FROM users WHERE username = ?", (session['username'],))
        is_admin = cursor.fetchone()[0]

        # Obtém o autor da postagem
        cursor.execute("SELECT author FROM posts WHERE id = ?", (post_id,))
        post_author = cursor.fetchone()

        # Verifica se o usuário é um administrador ou se é o autor da postagem
        if is_admin or (post_author and post_author[0] == session['username']):
            cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
            db.commit()
            flash('Postagem apagada com sucesso!', 'success')
        else:
            flash('Você não tem permissão para apagar esta postagem.', 'error')
        db.close()
    return redirect(url_for('index'))

# Rota para o formulário de cadastro de usuário
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            flash('Nome de usuário já está em uso. Escolha outro.', 'error')
        else:
            hashed_password = generate_password_hash(password)
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            db.commit()
            flash('Cadastro realizado com sucesso! Faça o login.', 'success')
            return redirect(url_for('login'))
        db.close()
    return render_template('register.html')

# Rota para o formulário de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        db.close()
        if user and check_password_hash(user[2], password):
            session['username'] = username
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha incorretos. Tente novamente.', 'error')
    return render_template('login.html')

# Rota para logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Você foi desconectado com sucesso.', 'success')
    return redirect(url_for('login'))

# Rota para renderizar o formulário de postagem privada
@app.route('/private_post_form')
def private_post_form():
    if 'username' in session:
        db = connect_db()
        cursor = db.cursor()

        # Verifica se o usuário é um administrador
        cursor.execute("SELECT is_admin FROM users WHERE username = ?", (session['username'],))
        is_admin_row = cursor.fetchone()
        if is_admin_row:
            is_admin = is_admin_row[0]
            app.logger.info("is_admin value: {}".format(is_admin))

            # Se o usuário for administrador, obtenha a lista de todos os usuários
            users = []
            if is_admin:
                cursor.execute("SELECT username FROM users")
                users = [row[0] for row in cursor.fetchall()]
                app.logger.info("Users: {}".format(users))

            db.close()

            if is_admin:
                return render_template('private_post_form.html', users=users)
            else:
                flash('Você não tem permissão para acessar esta página.', 'error')
                return redirect(url_for('index'))
    return redirect(url_for('login'))

# Rota para processar o envio da mensagem privada
@app.route('/post_private', methods=['POST'])
def post_private():
    if 'username' in session:
        content = request.form['content']
        recipient = request.form['recipient']
        author = session['username']

        # Validação dos dados
        if not content or not recipient:
            flash('Por favor, preencha todos os campos.', 'error')
            return redirect(url_for('private_post_form'))

        # Conectar ao banco de dados SQLite
        db = connect_db()
        cursor = db.cursor()

        # Inserir mensagem privada na tabela apropriada
        cursor.execute("INSERT INTO private_posts (content, recipient, author) VALUES (?, ?, ?)", (content, recipient, author))
        db.commit()
        db.close()

        flash('Mensagem privada enviada com sucesso para {}!'.format(recipient), 'success')
        return redirect(url_for('index'))
    return redirect(url_for('login'))

# Rota para exibir mensagens privadas
@app.route('/private_posts')
def private_posts():
    if 'username' in session:
        db = connect_db()
        cursor = db.cursor()

        # Obtém as mensagens privadas destinadas ao usuário logado
        cursor.execute("SELECT content, author FROM private_posts WHERE recipient = ?", (session['username'],))
        private_messages = cursor.fetchall()

        db.close()
        return render_template('private_posts.html', private_messages=private_messages)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
