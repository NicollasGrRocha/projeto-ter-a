from flask import Flask, request, redirect, url_for, render_template_string
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'LojaDB.db'

# ensure database and table

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jogos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            plataforma TEXT NOT NULL,
            quantidade INTEGER NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, preco, plataforma, quantidade FROM jogos')
    jogos = cursor.fetchall()
    conn.close()
    html = '''
    <style>
        .btn { background-color: #4CAF50; border: none; color: white; padding: 8px 12px; text-align: center; text-decoration: none; display: inline-block; font-size: 14px; margin: 2px 2px; cursor: pointer; border-radius: 5px; }
        .btn-primary { background-color: #3498db; }
        .btn-secondary { background-color: #6c757d; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ccc; padding: 8px; }
        th { background-color: #f5f5f5; }
    </style>
    <h1>Jogos Cadastrados</h1>
    <a class="btn btn-primary" href="{{ url_for('cadastrar') }}">Cadastrar novo jogo</a>
    <a class="btn btn-secondary" href="{{ url_for('clientes') }}">Ver clientes</a>
    <table>
        <tr><th>ID</th><th>Nome</th><th>Preço</th><th>Plataforma</th><th>Quantidade</th></tr>
        {% for jogo in jogos %}
        <tr>
            <td>{{ jogo[0] }}</td>
            <td>{{ jogo[1] }}</td>
            <td>{{ jogo[2] }}</td>
            <td>{{ jogo[3] }}</td>
            <td>{{ jogo[4] }}</td>
        </tr>
        {% endfor %}
    </table>
    '''
    return render_template_string(html, jogos=jogos)

@app.route('/cadastrar', methods=['GET','POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form.get('nome')
        preco = request.form.get('preco')
        plataforma = request.form.get('plataforma')
        quantidade = request.form.get('quantidade')
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO jogos (nome, preco, plataforma, quantidade) VALUES (?, ?, ?, ?)',
                       (nome, preco, plataforma, quantidade))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    html = '''
    <style>
        .btn { background-color: #4CAF50; border: none; color: white; padding: 8px 12px; text-align: center; text-decoration: none; display: inline-block; font-size: 14px; margin: 2px 2px; cursor: pointer; border-radius: 5px; }
        .btn-secondary { background-color: #6c757d; }
        form { max-width: 360px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ccc; padding: 8px; }
    </style>
    <h1>Cadastrar Jogo</h1>
    <form method="post">
        Nome:<br><input type="text" name="nome" required><br>
        Preço:<br><input type="number" step="0.01" name="preco" required><br>
        Plataforma:<br><input type="text" name="plataforma" required><br>
        Quantidade:<br><input type="number" name="quantidade" required><br><br>
        <input class="btn" type="submit" value="Cadastrar">
    </form>
    <a class="btn btn-secondary" href="{{ url_for('index') }}">Voltar</a>
    '''
    return render_template_string(html)

@app.route('/clientes')
def clientes():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, email, telefone FROM clientes')
    clientes = cursor.fetchall()
    conn.close()
    html = '''
    <style>
        .btn {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 8px 12px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 14px;
            margin: 2px 2px;
            cursor: pointer;
            border-radius: 5px;
        }
        .btn-danger { background-color: #e74c3c; }
        .btn-primary { background-color: #3498db; }
        .btn-secondary { background-color: #6c757d; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ccc; padding: 8px; }
        th { background-color: #f5f5f5; }
    </style>
    <h1>Clientes Cadastrados</h1>
    <a class="btn btn-primary" href="{{ url_for('cadastrar_cliente') }}">Cadastrar novo cliente</a>
    <a class="btn btn-secondary" href="{{ url_for('index') }}">Voltar para jogos</a>
    <table>
        <tr><th>ID</th><th>Nome</th><th>E-mail</th><th>Telefone</th><th>Ações</th></tr>
        {% for cliente in clientes %}
        <tr>
            <td>{{ cliente[0] }}</td>
            <td>{{ cliente[1] }}</td>
            <td>{{ cliente[2] }}</td>
            <td>{{ cliente[3] }}</td>
            <td>
                <a class="btn btn-danger" href="{{ url_for('deletar_cliente', cliente_id=cliente[0]) }}">Apagar</a>
            </td>
        </tr>
        {% endfor %}
    </table>
    '''
    return render_template_string(html, clientes=clientes)

@app.route('/clientes/cadastrar', methods=['GET','POST'])
def cadastrar_cliente():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)', (nome, email, telefone))
        conn.commit()
        conn.close()
        return redirect(url_for('clientes'))
    html = '''
    <style>
        .btn { background-color: #4CAF50; border: none; color: white; padding: 8px 12px; border-radius: 5px; font-size: 14px; cursor: pointer; text-decoration: none; }
        .btn-secondary { background-color: #6c757d; }
        form { max-width: 360px; }
    </style>
    <h1>Cadastrar Cliente</h1>
    <form method="post">
        Nome:<br><input type="text" name="nome" required><br>
        E-mail:<br><input type="email" name="email" required><br>
        Telefone:<br><input type="text" name="telefone" required><br><br>
        <input class="btn" type="submit" value="Cadastrar">
    </form>
    <a class="btn btn-secondary" href="{{ url_for('clientes') }}">Voltar</a>
    '''
    return render_template_string(html)

@app.route('/clientes/deletar/<int:cliente_id>')
def deletar_cliente(cliente_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clientes WHERE id = ?', (cliente_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('clientes'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
