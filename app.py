from flask import Flask, request, redirect, url_for, render_template_string
import sqlite3
import os
from datetime import datetime

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
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            jogo_id INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            data TEXT NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES clientes (id),
            FOREIGN KEY (jogo_id) REFERENCES jogos (id)
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
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Loja de Jogos - Início</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background: linear-gradient(135deg, #1e3c72, #2a5298);
                color: #fff;
                margin: 0;
                padding: 0;
                min-height: 100vh;
            }
            header {
                background: rgba(0, 0, 0, 0.8);
                padding: 20px;
                text-align: center;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            }
            header h1 {
                margin: 0;
                font-size: 2.5em;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            }
            nav {
                margin-top: 10px;
            }
            nav a {
                color: #fff;
                text-decoration: none;
                margin: 0 15px;
                padding: 10px 20px;
                background: #28a745;
                border-radius: 5px;
                transition: background 0.3s;
            }
            nav a:hover {
                background: #218838;
            }
            .container {
                max-width: 1200px;
                margin: 20px auto;
                padding: 20px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            }
            h1 {
                text-align: center;
                margin-bottom: 20px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                overflow: hidden;
            }
            th, td {
                padding: 15px;
                text-align: left;
                border-bottom: 1px solid rgba(255,255,255,0.2);
            }
            th {
                background: rgba(0,0,0,0.5);
                color: #fff;
            }
            tr:hover {
                background: rgba(255,255,255,0.1);
            }
            .btn {
                background: #007bff;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                text-decoration: none;
                display: inline-block;
                margin: 5px;
                transition: background 0.3s;
            }
            .btn:hover {
                background: #0056b3;
            }
            .btn-primary { background: #28a745; }
            .btn-primary:hover { background: #218838; }
            .btn-secondary { background: #6c757d; }
            .btn-secondary:hover { background: #5a6268; }
        </style>
    </head>
    <body>
        <header>
            <h1>🏆 Loja de Jogos 🏆</h1>
            <nav>
                <a href="{{ url_for('index') }}">Jogos</a>
                <a href="{{ url_for('clientes') }}">Clientes</a>
                <a href="{{ url_for('vendas') }}">Vendas</a>
            </nav>
        </header>
        <div class="container">
            <h1>Jogos Disponíveis</h1>
            <a class="btn btn-primary" href="{{ url_for('cadastrar') }}">Cadastrar Novo Jogo</a>
            <table>
                <tr><th>ID</th><th>Nome</th><th>Preço</th><th>Plataforma</th><th>Quantidade</th></tr>
                {% for jogo in jogos %}
                <tr>
                    <td>{{ jogo[0] }}</td>
                    <td>{{ jogo[1] }}</td>
                    <td>R$ {{ "%.2f"|format(jogo[2]) }}</td>
                    <td>{{ jogo[3] }}</td>
                    <td>{{ jogo[4] }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>
    </body>
    </html>
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
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Loja de Jogos - Cadastrar Jogo</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background: linear-gradient(135deg, #1e3c72, #2a5298);
                color: #fff;
                margin: 0;
                padding: 0;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
            }
            header {
                background: rgba(0, 0, 0, 0.8);
                padding: 20px;
                text-align: center;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            }
            header h1 {
                margin: 0;
                font-size: 2.5em;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            }
            nav {
                margin-top: 10px;
            }
            nav a {
                color: #fff;
                text-decoration: none;
                margin: 0 15px;
                padding: 10px 20px;
                background: #28a745;
                border-radius: 5px;
                transition: background 0.3s;
            }
            nav a:hover {
                background: #218838;
            }
            .container {
                max-width: 600px;
                margin: 20px auto;
                padding: 20px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
                flex: 1;
            }
            h1 {
                text-align: center;
                margin-bottom: 20px;
            }
            form {
                display: flex;
                flex-direction: column;
            }
            label {
                margin-bottom: 5px;
                font-weight: bold;
            }
            input, select {
                padding: 10px;
                margin-bottom: 15px;
                border: none;
                border-radius: 5px;
                background: rgba(255,255,255,0.9);
                color: #333;
            }
            .btn {
                background: #007bff;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                text-decoration: none;
                display: inline-block;
                margin: 5px;
                transition: background 0.3s;
                align-self: flex-start;
            }
            .btn:hover {
                background: #0056b3;
            }
            .btn-primary { background: #28a745; }
            .btn-primary:hover { background: #218838; }
            .btn-secondary { background: #6c757d; }
            .btn-secondary:hover { background: #5a6268; }
        </style>
    </head>
    <body>
        <header>
            <h1>🏆 Loja de Jogos 🏆</h1>
            <nav>
                <a href="{{ url_for('index') }}">Jogos</a>
                <a href="{{ url_for('clientes') }}">Clientes</a>
                <a href="{{ url_for('vendas') }}">Vendas</a>
            </nav>
        </header>
        <div class="container">
            <h1>Cadastrar Novo Jogo</h1>
            <form method="post">
                <label for="nome">Nome:</label>
                <input type="text" id="nome" name="nome" required>
                
                <label for="preco">Preço:</label>
                <input type="number" id="preco" name="preco" step="0.01" required>
                
                <label for="plataforma">Plataforma:</label>
                <input type="text" id="plataforma" name="plataforma" required>
                
                <label for="quantidade">Quantidade:</label>
                <input type="number" id="quantidade" name="quantidade" required>
                
                <input class="btn btn-primary" type="submit" value="Cadastrar">
                <a class="btn btn-secondary" href="{{ url_for('index') }}">Voltar</a>
            </form>
        </div>
    </body>
    </html>
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
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Loja de Jogos - Clientes</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background: linear-gradient(135deg, #1e3c72, #2a5298);
                color: #fff;
                margin: 0;
                padding: 0;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
            }
            header {
                background: rgba(0, 0, 0, 0.8);
                padding: 20px;
                text-align: center;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            }
            header h1 {
                margin: 0;
                font-size: 2.5em;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            }
            nav {
                margin-top: 10px;
            }
            nav a {
                color: #fff;
                text-decoration: none;
                margin: 0 15px;
                padding: 10px 20px;
                background: #28a745;
                border-radius: 5px;
                transition: background 0.3s;
            }
            nav a:hover {
                background: #218838;
            }
            .container {
                max-width: 1200px;
                margin: 20px auto;
                padding: 20px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
                flex: 1;
            }
            h1 {
                text-align: center;
                margin-bottom: 20px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                overflow: hidden;
            }
            th, td {
                padding: 15px;
                text-align: left;
                border-bottom: 1px solid rgba(255,255,255,0.2);
            }
            th {
                background: rgba(0,0,0,0.5);
                color: #fff;
            }
            tr:hover {
                background: rgba(255,255,255,0.1);
            }
            .btn {
                background: #007bff;
                color: white;
                padding: 8px 12px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                text-decoration: none;
                display: inline-block;
                margin: 2px;
                transition: background 0.3s;
            }
            .btn:hover {
                background: #0056b3;
            }
            .btn-primary { background: #28a745; }
            .btn-primary:hover { background: #218838; }
            .btn-secondary { background: #6c757d; }
            .btn-secondary:hover { background: #5a6268; }
            .btn-danger { background: #dc3545; }
            .btn-danger:hover { background: #c82333; }
        </style>
    </head>
    <body>
        <header>
            <h1>🏆 Loja de Jogos 🏆</h1>
            <nav>
                <a href="{{ url_for('index') }}">Jogos</a>
                <a href="{{ url_for('clientes') }}">Clientes</a>
                <a href="{{ url_for('vendas') }}">Vendas</a>
            </nav>
        </header>
        <div class="container">
            <h1>Clientes Cadastrados</h1>
            <a class="btn btn-primary" href="{{ url_for('cadastrar_cliente') }}">Cadastrar Novo Cliente</a>
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
        </div>
    </body>
    </html>
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
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Loja de Jogos - Cadastrar Cliente</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background: linear-gradient(135deg, #1e3c72, #2a5298);
                color: #fff;
                margin: 0;
                padding: 0;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
            }
            header {
                background: rgba(0, 0, 0, 0.8);
                padding: 20px;
                text-align: center;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            }
            header h1 {
                margin: 0;
                font-size: 2.5em;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            }
            nav {
                margin-top: 10px;
            }
            nav a {
                color: #fff;
                text-decoration: none;
                margin: 0 15px;
                padding: 10px 20px;
                background: #28a745;
                border-radius: 5px;
                transition: background 0.3s;
            }
            nav a:hover {
                background: #218838;
            }
            .container {
                max-width: 600px;
                margin: 20px auto;
                padding: 20px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
                flex: 1;
            }
            h1 {
                text-align: center;
                margin-bottom: 20px;
            }
            form {
                display: flex;
                flex-direction: column;
            }
            label {
                margin-bottom: 5px;
                font-weight: bold;
            }
            input, select {
                padding: 10px;
                margin-bottom: 15px;
                border: none;
                border-radius: 5px;
                background: rgba(255,255,255,0.9);
                color: #333;
            }
            .btn {
                background: #007bff;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                text-decoration: none;
                display: inline-block;
                margin: 5px;
                transition: background 0.3s;
                align-self: flex-start;
            }
            .btn:hover {
                background: #0056b3;
            }
            .btn-primary { background: #28a745; }
            .btn-primary:hover { background: #218838; }
            .btn-secondary { background: #6c757d; }
            .btn-secondary:hover { background: #5a6268; }
        </style>
    </head>
    <body>
        <header>
            <h1>🏆 Loja de Jogos 🏆</h1>
            <nav>
                <a href="{{ url_for('index') }}">Jogos</a>
                <a href="{{ url_for('clientes') }}">Clientes</a>
                <a href="{{ url_for('vendas') }}">Vendas</a>
            </nav>
        </header>
        <div class="container">
            <h1>Cadastrar Novo Cliente</h1>
            <form method="post">
                <label for="nome">Nome:</label>
                <input type="text" id="nome" name="nome" required>
                
                <label for="email">E-mail:</label>
                <input type="email" id="email" name="email" required>
                
                <label for="telefone">Telefone:</label>
                <input type="text" id="telefone" name="telefone" required>
                
                <input class="btn btn-primary" type="submit" value="Cadastrar">
                <a class="btn btn-secondary" href="{{ url_for('clientes') }}">Voltar</a>
            </form>
        </div>
    </body>
    </html>
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

@app.route('/vendas')
def vendas():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT v.id, c.nome, j.nome, v.quantidade, v.data
        FROM vendas v
        JOIN clientes c ON v.cliente_id = c.id
        JOIN jogos j ON v.jogo_id = j.id
    ''')
    vendas_list = cursor.fetchall()
    conn.close()
    html = '''
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Loja de Jogos - Vendas</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background: linear-gradient(135deg, #1e3c72, #2a5298);
                color: #fff;
                margin: 0;
                padding: 0;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
            }
            header {
                background: rgba(0, 0, 0, 0.8);
                padding: 20px;
                text-align: center;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            }
            header h1 {
                margin: 0;
                font-size: 2.5em;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            }
            nav {
                margin-top: 10px;
            }
            nav a {
                color: #fff;
                text-decoration: none;
                margin: 0 15px;
                padding: 10px 20px;
                background: #28a745;
                border-radius: 5px;
                transition: background 0.3s;
            }
            nav a:hover {
                background: #218838;
            }
            .container {
                max-width: 1200px;
                margin: 20px auto;
                padding: 20px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
                flex: 1;
            }
            h1 {
                text-align: center;
                margin-bottom: 20px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                overflow: hidden;
            }
            th, td {
                padding: 15px;
                text-align: left;
                border-bottom: 1px solid rgba(255,255,255,0.2);
            }
            th {
                background: rgba(0,0,0,0.5);
                color: #fff;
            }
            tr:hover {
                background: rgba(255,255,255,0.1);
            }
            .btn {
                background: #007bff;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                text-decoration: none;
                display: inline-block;
                margin: 5px;
                transition: background 0.3s;
            }
            .btn:hover {
                background: #0056b3;
            }
            .btn-primary { background: #28a745; }
            .btn-primary:hover { background: #218838; }
            .btn-secondary { background: #6c757d; }
            .btn-secondary:hover { background: #5a6268; }
        </style>
    </head>
    <body>
        <header>
            <h1>🏆 Loja de Jogos 🏆</h1>
            <nav>
                <a href="{{ url_for('index') }}">Jogos</a>
                <a href="{{ url_for('clientes') }}">Clientes</a>
                <a href="{{ url_for('vendas') }}">Vendas</a>
            </nav>
        </header>
        <div class="container">
            <h1>Vendas Registradas</h1>
            <a class="btn btn-primary" href="{{ url_for('registrar_venda') }}">Registrar Nova Venda</a>
            <table>
                <tr><th>ID</th><th>Cliente</th><th>Jogo</th><th>Quantidade</th><th>Data</th></tr>
                {% for venda in vendas_list %}
                <tr>
                    <td>{{ venda[0] }}</td>
                    <td>{{ venda[1] }}</td>
                    <td>{{ venda[2] }}</td>
                    <td>{{ venda[3] }}</td>
                    <td>{{ venda[4] }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html, vendas_list=vendas_list)

@app.route('/vendas/registrar', methods=['GET','POST'])
def registrar_venda():
    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id')
        jogo_id = request.form.get('jogo_id')
        quantidade = int(request.form.get('quantidade'))
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        # Check stock
        cursor.execute('SELECT quantidade FROM jogos WHERE id = ?', (jogo_id,))
        stock = cursor.fetchone()[0]
        if quantidade > stock:
            conn.close()
            return "Erro: Quantidade insuficiente em estoque."
        # Insert venda
        data = str(datetime.now())
        cursor.execute('INSERT INTO vendas (cliente_id, jogo_id, quantidade, data) VALUES (?, ?, ?, ?)',
                       (cliente_id, jogo_id, quantidade, data))
        # Update stock
        cursor.execute('UPDATE jogos SET quantidade = quantidade - ? WHERE id = ?', (quantidade, jogo_id))
        conn.commit()
        conn.close()
        return redirect(url_for('vendas'))
    # GET: show form
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome FROM clientes')
    clientes = cursor.fetchall()
    cursor.execute('SELECT id, nome FROM jogos')
    jogos = cursor.fetchall()
    conn.close()
    html = '''
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Loja de Jogos - Registrar Venda</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background: linear-gradient(135deg, #1e3c72, #2a5298);
                color: #fff;
                margin: 0;
                padding: 0;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
            }
            header {
                background: rgba(0, 0, 0, 0.8);
                padding: 20px;
                text-align: center;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            }
            header h1 {
                margin: 0;
                font-size: 2.5em;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            }
            nav {
                margin-top: 10px;
            }
            nav a {
                color: #fff;
                text-decoration: none;
                margin: 0 15px;
                padding: 10px 20px;
                background: #28a745;
                border-radius: 5px;
                transition: background 0.3s;
            }
            nav a:hover {
                background: #218838;
            }
            .container {
                max-width: 600px;
                margin: 20px auto;
                padding: 20px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
                flex: 1;
            }
            h1 {
                text-align: center;
                margin-bottom: 20px;
            }
            form {
                display: flex;
                flex-direction: column;
            }
            label {
                margin-bottom: 5px;
                font-weight: bold;
            }
            input, select {
                padding: 10px;
                margin-bottom: 15px;
                border: none;
                border-radius: 5px;
                background: rgba(255,255,255,0.9);
                color: #333;
            }
            .btn {
                background: #007bff;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                text-decoration: none;
                display: inline-block;
                margin: 5px;
                transition: background 0.3s;
                align-self: flex-start;
            }
            .btn:hover {
                background: #0056b3;
            }
            .btn-primary { background: #28a745; }
            .btn-primary:hover { background: #218838; }
            .btn-secondary { background: #6c757d; }
            .btn-secondary:hover { background: #5a6268; }
        </style>
    </head>
    <body>
        <header>
            <h1>🏆 Loja de Jogos 🏆</h1>
            <nav>
                <a href="{{ url_for('index') }}">Jogos</a>
                <a href="{{ url_for('clientes') }}">Clientes</a>
                <a href="{{ url_for('vendas') }}">Vendas</a>
            </nav>
        </header>
        <div class="container">
            <h1>Registrar Venda</h1>
            <form method="post">
                <label for="cliente_id">Cliente:</label>
                <select id="cliente_id" name="cliente_id" required>
                    {% for cliente in clientes %}
                    <option value="{{ cliente[0] }}">{{ cliente[1] }}</option>
                    {% endfor %}
                </select>
                
                <label for="jogo_id">Jogo:</label>
                <select id="jogo_id" name="jogo_id" required>
                    {% for jogo in jogos %}
                    <option value="{{ jogo[0] }}">{{ jogo[1] }}</option>
                    {% endfor %}
                </select>
                
                <label for="quantidade">Quantidade:</label>
                <input type="number" id="quantidade" name="quantidade" min="1" required>
                
                <input class="btn btn-primary" type="submit" value="Registrar">
                <a class="btn btn-secondary" href="{{ url_for('vendas') }}">Voltar</a>
            </form>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html, clientes=clientes, jogos=jogos)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
