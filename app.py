from flask import Flask, request, redirect, url_for, render_template_string
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
DATABASE = 'LojaDB.db'
LOW_STOCK_THRESHOLD = 5

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
    return redirect(url_for('user_home'))

@app.route('/user')
def user_home():
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
        <title>Loja de Jogos - Usuário</title>
        <style>
            body {
                font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: radial-gradient(circle at top left, rgba(40, 108, 201, 0.88), transparent 26%),
                            linear-gradient(135deg, #071a3d 0%, #112d5d 45%, #14366f 100%);
                color: #f3f7ff;
                margin: 0;
                padding: 0;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            * {
                box-sizing: border-box;
            }
            header {
                width: 100%;
                background: rgba(5, 18, 52, 0.94);
                padding: 18px 0;
                text-align: center;
                box-shadow: 0 20px 70px rgba(1,16,58,0.34);
                border-bottom: 1px solid rgba(255,255,255,0.08);
                position: sticky;
                top: 0;
                z-index: 10;
            }
            header h1 {
                margin: 0;
                font-size: 2.4rem;
                line-height: 1.05;
                text-shadow: 0 4px 18px rgba(0,0,0,0.35);
            }
            nav {
                margin-top: 14px;
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                gap: 12px;
            }
            nav a {
                color: #fff;
                text-decoration: none;
                padding: 12px 24px;
                background: rgba(255,255,255,0.1);
                border-radius: 999px;
                border: 1px solid rgba(255,255,255,0.14);
                transition: transform 0.25s ease, background 0.25s ease, border-color 0.25s ease;
                font-weight: 600;
            }
            nav a:hover {
                background: rgba(255,255,255,0.18);
                transform: translateY(-1px);
                border-color: rgba(255,255,255,0.22);
            }
            .container, .main-container {
                width: min(1120px, 100%);
                margin: 32px auto 40px;
                padding: 32px;
                background: rgba(8, 20, 54, 0.88);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 28px;
                box-shadow: 0 35px 90px rgba(0,0,0,0.23);
                backdrop-filter: blur(14px);
            }
            .container {
                text-align: center;
            }
            .card-behind {
                display: inline-block;
                padding: 12px 18px;
                border-radius: 18px;
                background: rgba(8, 28, 90, 0.96);
                box-shadow: 0 18px 38px rgba(2,14,55,0.38);
                color: #f8fafc;
                margin-bottom: 18px;
            }
            h1, h2, h3 {
                margin: 0 0 20px;
            }
            h2 {
                color: #dbeafe;
            }
            .section-title {
                grid-column: 1 / -1;
                margin: 0 0 14px;
                font-size: 1.2rem;
                letter-spacing: 0.02em;
            }
            .filters, .summary, .actions, .form-grid {
                display: grid;
                gap: 16px;
            }
            .filters {
                background: rgba(255,255,255,0.08);
                border: 1px solid rgba(255,255,255,0.12);
                padding: 24px;
                border-radius: 22px;
            }
            .filter-row {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 16px;
                align-items: end;
            }
            .filter-group {
                display: flex;
                flex-direction: column;
                text-align: left;
            }
            .filter-group label,
            label {
                margin-bottom: 8px;
                font-weight: 600;
                color: #e2e8f0;
            }
            .filter-group input,
            .filter-group select,
            input,
            select,
            textarea {
                width: 100%;
                padding: 14px 16px;
                border-radius: 16px;
                border: 1px solid rgba(255,255,255,0.14);
                background: rgba(255,255,255,0.96);
                color: #1f2937;
                transition: border-color 0.25s ease, box-shadow 0.25s ease;
            }
            input:focus,
            select:focus,
            textarea:focus {
                outline: none;
                border-color: rgba(96,165,250,0.85);
                box-shadow: 0 0 0 4px rgba(59,130,246,0.12);
            }
            .form-actions,
            .actions {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 14px;
                margin-top: 18px;
            }
            .btn {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                gap: 0.5rem;
                padding: 12px 22px;
                border: none;
                border-radius: 999px;
                cursor: pointer;
                text-decoration: none;
                color: #fff;
                transition: transform 0.2s ease, filter 0.2s ease, background 0.25s ease;
                font-weight: 700;
            }
            .btn:hover {
                transform: translateY(-1px);
                filter: brightness(1.05);
            }
            .btn-primary { background: #2563eb; }
            .btn-primary:hover { background: #1d4ed8; }
            .btn-secondary {
                background: #475569;
                border: 1px solid rgba(255,255,255,0.18);
                color: #eff6ff;
            }
            .btn-secondary:hover {
                background: #334155;
            }
            .btn-danger { background: #ef4444; }
            .btn-danger:hover { background: #dc2626; }
            .btn-small {
                padding: 10px 16px;
                border-radius: 14px;
            }
            .btn-block {
                width: 100%;
            }
            .table-card {
                overflow: hidden;
                border-radius: 24px;
                border: 1px solid rgba(255,255,255,0.08);
                box-shadow: inset 0 0 0 1px rgba(255,255,255,0.02);
            }
            table {
                width: 100%;
                border-collapse: separate;
                border-spacing: 0;
                margin-top: 22px;
                border-radius: 18px;
                overflow: hidden;
                background: rgba(255,255,255,0.04);
            }
            th, td {
                padding: 16px 18px;
                background: rgba(255,255,255,0.06);
                border-bottom: 1px solid rgba(255,255,255,0.08);
                color: #eff6ff;
            }
            th {
                background: rgba(255,255,255,0.12);
                font-weight: 700;
                letter-spacing: 0.03em;
            }
            tr:hover {
                background: rgba(255,255,255,0.08);
            }
            .low-stock {
                background: rgba(248, 113, 113, 0.16);
            }
            .stock-warning {
                padding: 20px;
                border-radius: 22px;
                background: rgba(248, 113, 113, 0.14);
                border: 1px solid rgba(248, 113, 113, 0.18);
                box-shadow: inset 0 0 0 1px rgba(255,255,255,0.05);
                text-align: left;
            }
            .summary {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 18px;
                margin-top: 18px;
            }
            .summary .card {
                padding: 20px;
                border-radius: 24px;
                background: rgba(255,255,255,0.08);
                border: 1px solid rgba(255,255,255,0.12);
                box-shadow: 0 20px 40px rgba(0,0,0,0.12);
                text-align: left;
            }
            .summary .card strong {
                display: block;
                margin-bottom: 12px;
                color: #dbeafe;
            }
            .metric-value,
            .metric-detail {
                margin-top: 12px;
                font-size: 1.35rem;
                color: #e2e8f0;
                line-height: 1.4;
            }
            .empty-row td {
                text-align: center;
                padding: 20px;
            }
            .footer-note {
                margin-top: 24px;
                font-size: 0.95rem;
                color: rgba(226,232,240,0.68);
            }
        </style>
        </head>
    <body>
        <header>
            <h1 class="card-behind">🏆 Loja de Jogos - Usuário 🏆</h1>
            <nav>
                <a href="{{ url_for('user_home') }}">Home</a>
                <a href="{{ url_for('registrar_venda') }}">Comprar Jogo</a>
                <a href="{{ url_for('admin_home') }}">Admin</a>
            </nav>
        </header>
        <div class="container">
            <h1 class="card-behind">Jogos Disponíveis</h1>
            <a class="btn btn-secondary" href="{{ url_for('registrar_venda') }}">Registrar Compra</a>
            <a class="btn btn-secondary" href="{{ url_for('admin_home') }}">Acesso Admin</a>
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

@app.route('/admin')
def admin_home():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Get filter parameters
    nome_filtro = request.args.get('nome', '').strip()
    plataforma_filtro = request.args.get('plataforma', '').strip()
    quantidade_filtro = request.args.get('quantidade', '').strip()
    
    # Build base query
    query = 'SELECT id, nome, preco, plataforma, quantidade FROM jogos WHERE 1=1'
    params = []
    
    # Apply filters
    if nome_filtro:
        query += ' AND nome LIKE ?'
        params.append(f'%{nome_filtro}%')
    
    if plataforma_filtro:
        query += ' AND plataforma LIKE ?'
        params.append(f'%{plataforma_filtro}%')
    
    if quantidade_filtro:
        try:
            qty = int(quantidade_filtro)
            query += ' AND quantidade = ?'
            params.append(qty)
        except ValueError:
            pass
    
    query += ' ORDER BY quantidade ASC'
    cursor.execute(query, params)
    jogos = cursor.fetchall()
    
    # Get low stock items
    cursor.execute('SELECT id, nome, preco, plataforma, quantidade FROM jogos WHERE quantidade <= ?', (LOW_STOCK_THRESHOLD,))
    low_stock = cursor.fetchall()
    
    conn.close()
    
    html = '''
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Loja de Jogos - Admin</title>
        <style>
            body {
                font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: radial-gradient(circle at top left, rgba(40, 108, 201, 0.88), transparent 26%),
                            linear-gradient(135deg, #071a3d 0%, #112d5d 45%, #14366f 100%);
                color: #f3f7ff;
                margin: 0;
                padding: 0;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            * {
                box-sizing: border-box;
            }
            header {
                width: 100%;
                background: rgba(5, 18, 52, 0.94);
                padding: 18px 0;
                text-align: center;
                box-shadow: 0 20px 70px rgba(1,16,58,0.34);
                border-bottom: 1px solid rgba(255,255,255,0.08);
                position: sticky;
                top: 0;
                z-index: 10;
            }
            header h1 {
                margin: 0;
                font-size: 2.4rem;
                line-height: 1.05;
                text-shadow: 0 4px 18px rgba(0,0,0,0.35);
            }
            nav {
                margin-top: 14px;
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                gap: 12px;
            }
            nav a {
                color: #fff;
                text-decoration: none;
                padding: 12px 24px;
                background: rgba(255,255,255,0.1);
                border-radius: 999px;
                border: 1px solid rgba(255,255,255,0.14);
                transition: transform 0.25s ease, background 0.25s ease, border-color 0.25s ease;
                font-weight: 600;
            }
            nav a:hover {
                background: rgba(255,255,255,0.18);
                transform: translateY(-1px);
                border-color: rgba(255,255,255,0.22);
            }
            .container, .main-container {
                width: min(1120px, 100%);
                margin: 32px auto 40px;
                padding: 32px;
                background: rgba(8, 20, 54, 0.88);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 28px;
                box-shadow: 0 35px 90px rgba(0,0,0,0.23);
                backdrop-filter: blur(14px);
            }
            .container {
                text-align: center;
            }
            .card-behind {
                display: inline-block;
                padding: 12px 18px;
                border-radius: 18px;
                background: rgba(8, 28, 90, 0.96);
                box-shadow: 0 18px 38px rgba(2,14,55,0.38);
                color: #f8fafc;
                margin-bottom: 18px;
            }
            h1, h2, h3 {
                margin: 0 0 20px;
            }
            h2 {
                color: #dbeafe;
            }
            .section-title {
                grid-column: 1 / -1;
                margin: 0 0 14px;
                font-size: 1.2rem;
                letter-spacing: 0.02em;
            }
            .filters, .summary, .actions, .form-grid {
                display: grid;
                gap: 16px;
            }
            .filters {
                background: rgba(255,255,255,0.08);
                border: 1px solid rgba(255,255,255,0.12);
                padding: 24px;
                border-radius: 22px;
            }
            .filter-row {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 16px;
                align-items: end;
            }
            .filter-group {
                display: flex;
                flex-direction: column;
                text-align: left;
            }
            .filter-group label,
            label {
                margin-bottom: 8px;
                font-weight: 600;
                color: #e2e8f0;
            }
            .filter-group input,
            .filter-group select,
            input,
            select,
            textarea {
                width: 100%;
                padding: 14px 16px;
                border-radius: 16px;
                border: 1px solid rgba(255,255,255,0.14);
                background: rgba(255,255,255,0.96);
                color: #1f2937;
                transition: border-color 0.25s ease, box-shadow 0.25s ease;
            }
            input:focus,
            select:focus,
            textarea:focus {
                outline: none;
                border-color: rgba(96,165,250,0.85);
                box-shadow: 0 0 0 4px rgba(59,130,246,0.12);
            }
            .form-actions,
            .actions {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 14px;
                margin-top: 18px;
            }
            .btn {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                gap: 0.5rem;
                padding: 12px 22px;
                border: none;
                border-radius: 999px;
                cursor: pointer;
                text-decoration: none;
                color: #fff;
                transition: transform 0.2s ease, filter 0.2s ease, background 0.25s ease;
                font-weight: 700;
            }
            .btn:hover {
                transform: translateY(-1px);
                filter: brightness(1.05);
            }
            .btn-primary { background: #2563eb; }
            .btn-primary:hover { background: #1d4ed8; }
            .btn-secondary {
                background: #475569;
                border: 1px solid rgba(255,255,255,0.18);
                color: #eff6ff;
            }
            .btn-secondary:hover {
                background: #334155;
            }
            .btn-danger { background: #ef4444; }
            .btn-danger:hover { background: #dc2626; }
            .btn-small {
                padding: 10px 16px;
                border-radius: 14px;
            }
            .btn-block {
                width: 100%;
            }
            .table-card {
                overflow: hidden;
                border-radius: 24px;
                border: 1px solid rgba(255,255,255,0.08);
                box-shadow: inset 0 0 0 1px rgba(255,255,255,0.02);
            }
            table {
                width: 100%;
                border-collapse: separate;
                border-spacing: 0;
                margin-top: 22px;
                border-radius: 18px;
                overflow: hidden;
                background: rgba(255,255,255,0.04);
            }
            th, td {
                padding: 16px 18px;
                background: rgba(255,255,255,0.06);
                border-bottom: 1px solid rgba(255,255,255,0.08);
                color: #eff6ff;
            }
            th {
                background: rgba(255,255,255,0.12);
                font-weight: 700;
                letter-spacing: 0.03em;
            }
            tr:hover {
                background: rgba(255,255,255,0.08);
            }
            .low-stock {
                background: rgba(248, 113, 113, 0.16);
            }
            .stock-warning {
                padding: 20px;
                border-radius: 22px;
                background: rgba(248, 113, 113, 0.14);
                border: 1px solid rgba(248, 113, 113, 0.18);
                box-shadow: inset 0 0 0 1px rgba(255,255,255,0.05);
                text-align: left;
            }
            .summary {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 18px;
                margin-top: 18px;
            }
            .summary .card {
                padding: 20px;
                border-radius: 24px;
                background: rgba(255,255,255,0.08);
                border: 1px solid rgba(255,255,255,0.12);
                box-shadow: 0 20px 40px rgba(0,0,0,0.12);
                text-align: left;
            }
            .summary .card strong {
                display: block;
                margin-bottom: 12px;
                color: #dbeafe;
            }
            .metric-value,
            .metric-detail {
                margin-top: 12px;
                font-size: 1.35rem;
                color: #e2e8f0;
                line-height: 1.4;
            }
            .empty-row td {
                text-align: center;
                padding: 20px;
            }
            .footer-note {
                margin-top: 24px;
                font-size: 0.95rem;
                color: rgba(226,232,240,0.68);
            }
        </style>
    </head>
    <body>
        <header>
            <h1 class="card-behind">🏆 Loja de Jogos - Admin 🏆</h1>
            <nav>
                <a href="{{ url_for('admin_home') }}">Admin</a>
                <a href="{{ url_for('user_home') }}">Usuário</a>
            </nav>
        </header>
        <div class="container">
            <h1 class="card-behind">Dashboard do Administrador</h1>
            <div class="actions">
                <a class="btn btn-primary" href="{{ url_for('cadastrar') }}">Cadastrar Jogo</a>
                <a class="btn btn-primary" href="{{ url_for('clientes') }}">Gerenciar Clientes</a>
                <a class="btn btn-primary" href="{{ url_for('vendas') }}">Ver Vendas</a>
                <a class="btn btn-secondary" href="{{ url_for('controle_estoque') }}">Ver Estoque</a>
                <a class="btn btn-secondary" href="{{ url_for('relatorio') }}">Relatório</a>
            </div>
            
            <!-- Filtros -->
            <div class="filters">
                <h2 class="section-title">🔍 Filtros</h2>
                <form method="get" class="form-grid">
                    <div class="filter-group">
                        <label for="nome">Nome do Jogo:</label>
                        <input type="text" id="nome" name="nome" value="{{ nome_filtro }}" placeholder="Buscar por nome...">
                    </div>
                    
                    <div class="filter-group">
                        <label for="plataforma">Plataforma:</label>
                        <input type="text" id="plataforma" name="plataforma" value="{{ plataforma_filtro }}" placeholder="Ex: PC, PS5, Xbox...">
                    </div>
                    
                    <div class="filter-group">
                        <label for="quantidade">Quantidade:</label>
                        <input type="number" id="quantidade" name="quantidade" value="{{ quantidade_filtro }}" placeholder="Ex: 10">
                    </div>
                    
                    <div class="form-actions">
                        <button type="submit" class="btn btn-primary btn-block">Filtrar</button>
                        <a href="{{ url_for('admin_home') }}" class="btn btn-secondary btn-block">Limpar</a>
                    </div>
                </form>
            </div>
            
            {% if low_stock %}
            <div class="stock-warning">
                <h2>⚠️ Jogos com estoque baixo</h2>
                <table>
                    <tr><th>ID</th><th>Nome</th><th>Plataforma</th><th>Quantidade</th><th>Ações</th></tr>
                    {% for jogo in low_stock %}
                    <tr>
                        <td>{{ jogo[0] }}</td>
                        <td>{{ jogo[1] }}</td>
                        <td>{{ jogo[3] }}</td>
                        <td>{{ jogo[4] }}</td>
                        <td><a class="btn btn-secondary btn-small" href="{{ url_for('atualizar_quantidade', jogo_id=jogo[0]) }}">Atualizar</a></td>
                    </tr>
                    {% endfor %}
                </table>
            </div>
            {% endif %}
            
            <h2 class="section-title">Total de jogos: {{ jogos|length }}</h2>
            <table>
                <tr><th>ID</th><th>Nome</th><th>Preço</th><th>Plataforma</th><th>Quantidade</th><th>Ações</th></tr>
                {% if jogos %}
                    {% for jogo in jogos %}
                    <tr class="{% if jogo[4] <= low_threshold %}low-stock{% endif %}">
                        <td>{{ jogo[0] }}</td>
                        <td>{{ jogo[1] }}</td>
                        <td>R$ {{ "%.2f"|format(jogo[2]) }}</td>
                        <td>{{ jogo[3] }}</td>
                        <td>{{ jogo[4] }}</td>
                        <td><a class="btn btn-secondary btn-small" href="{{ url_for('atualizar_quantidade', jogo_id=jogo[0]) }}">Atualizar</a></td>
                    </tr>
                    {% endfor %}
                {% else %}
                    <tr><td colspan="6" class="empty-row">Nenhum jogo encontrado com os filtros aplicados</td></tr>
                {% endif %}
            </table>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html, jogos=jogos, low_stock=low_stock, low_threshold=LOW_STOCK_THRESHOLD, 
                                 nome_filtro=nome_filtro, plataforma_filtro=plataforma_filtro, 
                                 quantidade_filtro=quantidade_filtro)

@app.route('/estoque')
def controle_estoque():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, preco, plataforma, quantidade FROM jogos ORDER BY quantidade ASC')
    jogos = cursor.fetchall()
    cursor.execute('SELECT id, nome, preco, plataforma, quantidade FROM jogos WHERE quantidade <= ?', (LOW_STOCK_THRESHOLD,))
    low_stock = cursor.fetchall()
    conn.close()
    html = '''
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Loja de Jogos - Controle de Estoque</title>
        <style>
            body {
                font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: radial-gradient(circle at top left, rgba(40, 108, 201, 0.88), transparent 26%),
                            linear-gradient(135deg, #071a3d 0%, #112d5d 45%, #14366f 100%);
                color: #f3f7ff;
                margin: 0;
                padding: 0;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            * {
                box-sizing: border-box;
            }
            header {
                width: 100%;
                background: rgba(5, 18, 52, 0.94);
                padding: 18px 0;
                text-align: center;
                box-shadow: 0 20px 70px rgba(1,16,58,0.34);
                border-bottom: 1px solid rgba(255,255,255,0.08);
                position: sticky;
                top: 0;
                z-index: 10;
            }
            header h1 {
                margin: 0;
                font-size: 2.4rem;
                line-height: 1.05;
                text-shadow: 0 4px 18px rgba(0,0,0,0.35);
            }
            nav {
                margin-top: 14px;
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                gap: 12px;
            }
            nav a {
                color: #fff;
                text-decoration: none;
                padding: 12px 24px;
                background: rgba(255,255,255,0.1);
                border-radius: 999px;
                border: 1px solid rgba(255,255,255,0.14);
                transition: transform 0.25s ease, background 0.25s ease, border-color 0.25s ease;
                font-weight: 600;
            }
            nav a:hover {
                background: rgba(255,255,255,0.18);
                transform: translateY(-1px);
                border-color: rgba(255,255,255,0.22);
            }
            .container, .main-container {
                width: min(1120px, 100%);
                margin: 32px auto 40px;
                padding: 32px;
                background: rgba(8, 20, 54, 0.88);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 28px;
                box-shadow: 0 35px 90px rgba(0,0,0,0.23);
                backdrop-filter: blur(14px);
            }
            .container {
                text-align: center;
            }
            .card-behind {
                display: inline-block;
                padding: 12px 18px;
                border-radius: 18px;
                background: rgba(8, 28, 90, 0.96);
                box-shadow: 0 18px 38px rgba(2,14,55,0.38);
                color: #f8fafc;
                margin-bottom: 18px;
            }
            h1, h2, h3 {
                margin: 0 0 20px;
            }
            h2 {
                color: #dbeafe;
            }
            .section-title {
                grid-column: 1 / -1;
                margin: 0 0 14px;
                font-size: 1.2rem;
                letter-spacing: 0.02em;
            }
            .filters, .summary, .actions, .form-grid {
                display: grid;
                gap: 16px;
            }
            .filters {
                background: rgba(255,255,255,0.08);
                border: 1px solid rgba(255,255,255,0.12);
                padding: 24px;
                border-radius: 22px;
            }
            .filter-row {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 16px;
                align-items: end;
            }
            .filter-group {
                display: flex;
                flex-direction: column;
                text-align: left;
            }
            .filter-group label,
            label {
                margin-bottom: 8px;
                font-weight: 600;
                color: #e2e8f0;
            }
            .filter-group input,
            .filter-group select,
            input,
            select,
            textarea {
                width: 100%;
                padding: 14px 16px;
                border-radius: 16px;
                border: 1px solid rgba(255,255,255,0.14);
                background: rgba(255,255,255,0.96);
                color: #1f2937;
                transition: border-color 0.25s ease, box-shadow 0.25s ease;
            }
            input:focus,
            select:focus,
            textarea:focus {
                outline: none;
                border-color: rgba(96,165,250,0.85);
                box-shadow: 0 0 0 4px rgba(59,130,246,0.12);
            }
            .form-actions,
            .actions {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 14px;
                margin-top: 18px;
            }
            .btn {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                gap: 0.5rem;
                padding: 12px 22px;
                border: none;
                border-radius: 999px;
                cursor: pointer;
                text-decoration: none;
                color: #fff;
                transition: transform 0.2s ease, filter 0.2s ease, background 0.25s ease;
                font-weight: 700;
            }
            .btn:hover {
                transform: translateY(-1px);
                filter: brightness(1.05);
            }
            .btn-primary { background: #2563eb; }
            .btn-primary:hover { background: #1d4ed8; }
            .btn-secondary {
                background: #475569;
                border: 1px solid rgba(255,255,255,0.18);
                color: #eff6ff;
            }
            .btn-secondary:hover {
                background: #334155;
            }
            .btn-danger { background: #ef4444; }
            .btn-danger:hover { background: #dc2626; }
            .btn-small {
                padding: 10px 16px;
                border-radius: 14px;
            }
            .btn-block {
                width: 100%;
            }
            .table-card {
                overflow: hidden;
                border-radius: 24px;
                border: 1px solid rgba(255,255,255,0.08);
                box-shadow: inset 0 0 0 1px rgba(255,255,255,0.02);
            }
            table {
                width: 100%;
                border-collapse: separate;
                border-spacing: 0;
                margin-top: 22px;
                border-radius: 18px;
                overflow: hidden;
                background: rgba(255,255,255,0.04);
            }
            th, td {
                padding: 16px 18px;
                background: rgba(255,255,255,0.06);
                border-bottom: 1px solid rgba(255,255,255,0.08);
                color: #eff6ff;
            }
            th {
                background: rgba(255,255,255,0.12);
                font-weight: 700;
                letter-spacing: 0.03em;
            }
            tr:hover {
                background: rgba(255,255,255,0.08);
            }
            .low-stock {
                background: rgba(248, 113, 113, 0.16);
            }
            .stock-warning {
                padding: 20px;
                border-radius: 22px;
                background: rgba(248, 113, 113, 0.14);
                border: 1px solid rgba(248, 113, 113, 0.18);
                box-shadow: inset 0 0 0 1px rgba(255,255,255,0.05);
                text-align: left;
            }
            .summary {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 18px;
                margin-top: 18px;
            }
            .summary .card {
                padding: 20px;
                border-radius: 24px;
                background: rgba(255,255,255,0.08);
                border: 1px solid rgba(255,255,255,0.12);
                box-shadow: 0 20px 40px rgba(0,0,0,0.12);
                text-align: left;
            }
            .summary .card strong {
                display: block;
                margin-bottom: 12px;
                color: #dbeafe;
            }
            .metric-value,
            .metric-detail {
                margin-top: 12px;
                font-size: 1.35rem;
                color: #e2e8f0;
                line-height: 1.4;
            }
            .empty-row td {
                text-align: center;
                padding: 20px;
            }
            .footer-note {
                margin-top: 24px;
                font-size: 0.95rem;
                color: rgba(226,232,240,0.68);
            }
        </style>
    </head>
    <body>
        <header>
            <h1 class="card-behind">🏆 Loja de Jogos 🏆</h1>
            <nav>
                <a href="{{ url_for('index') }}">Jogos</a>
                <a href="{{ url_for('clientes') }}">Clientes</a>
                
                <a href="{{ url_for('controle_estoque') }}">Estoque</a>
                <a href="{{ url_for('admin_home') }}">Admin</a>
            </nav>
        </header>
        <div class="container">
            <h1 class="card-behind">Controle de Estoque</h1>
            {% if low_stock %}
            <div class="stock-warning">
                <h2>⚠️ Jogos com estoque baixo</h2>
                <table>
                    <tr><th>ID</th><th>Nome</th><th>Plataforma</th><th>Quantidade</th><th>Ações</th></tr>
                    {% for jogo in low_stock %}
                    <tr class="low-stock">
                        <td>{{ jogo[0] }}</td>
                        <td>{{ jogo[1] }}</td>
                        <td>{{ jogo[3] }}</td>
                        <td>{{ jogo[4] }}</td>
                        <td><a class="btn btn-secondary" href="{{ url_for('atualizar_quantidade', jogo_id=jogo[0]) }}">Atualizar</a></td>
                    </tr>
                    {% endfor %}
                </table>
            </div>
            {% endif %}
            <table>
                <tr><th>ID</th><th>Nome</th><th>Preço</th><th>Plataforma</th><th>Quantidade</th><th>Ações</th></tr>
                {% for jogo in jogos %}
                <tr class="{% if jogo[4] <= low_threshold %}low-stock{% endif %}">
                    <td>{{ jogo[0] }}</td>
                    <td>{{ jogo[1] }}</td>
                    <td>R$ {{ "%.2f"|format(jogo[2]) }}</td>
                    <td>{{ jogo[3] }}</td>
                    <td>{{ jogo[4] }}</td>
                    <td><a class="btn btn-secondary" href="{{ url_for('atualizar_quantidade', jogo_id=jogo[0]) }}">Atualizar</a></td>
                </tr>
                {% endfor %}
            </table>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html, jogos=jogos, low_stock=low_stock, low_threshold=LOW_STOCK_THRESHOLD)

@app.route('/jogos/atualizar/<int:jogo_id>', methods=['GET','POST'])
def atualizar_quantidade(jogo_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    if request.method == 'POST':
        try:
            quantidade = int(request.form.get('quantidade', 0))
        except ValueError:
            quantidade = 0
        if quantidade < 0:
            quantidade = 0
        cursor.execute('UPDATE jogos SET quantidade = ? WHERE id = ?', (quantidade, jogo_id))
        conn.commit()
        conn.close()
        return redirect(url_for('controle_estoque'))
    cursor.execute('SELECT id, nome, plataforma, quantidade FROM jogos WHERE id = ?', (jogo_id,))
    jogo = cursor.fetchone()
    conn.close()
    if not jogo:
        return redirect(url_for('controle_estoque'))
    html = '''
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Atualizar Quantidade</title>
        <style>
            body {
                font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: radial-gradient(circle at top left, rgba(40, 108, 201, 0.88), transparent 26%),
                            linear-gradient(135deg, #071a3d 0%, #112d5d 45%, #14366f 100%);
                color: #f3f7ff;
                margin: 0;
                padding: 0;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            * {
                box-sizing: border-box;
            }
            header {
                width: 100%;
                background: rgba(5, 18, 52, 0.94);
                padding: 18px 0;
                text-align: center;
                box-shadow: 0 20px 70px rgba(1,16,58,0.34);
                border-bottom: 1px solid rgba(255,255,255,0.08);
                position: sticky;
                top: 0;
                z-index: 10;
            }
            header h1 {
                margin: 0;
                font-size: 2.4rem;
                line-height: 1.05;
                text-shadow: 0 4px 18px rgba(0,0,0,0.35);
            }
            nav {
                margin-top: 14px;
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                gap: 12px;
            }
            nav a {
                color: #fff;
                text-decoration: none;
                padding: 12px 24px;
                background: rgba(255,255,255,0.1);
                border-radius: 999px;
                border: 1px solid rgba(255,255,255,0.14);
                transition: transform 0.25s ease, background 0.25s ease, border-color 0.25s ease;
                font-weight: 600;
            }
            nav a:hover {
                background: rgba(255,255,255,0.18);
                transform: translateY(-1px);
                border-color: rgba(255,255,255,0.22);
            }
            .container, .main-container {
                width: min(1120px, 100%);
                margin: 32px auto 40px;
                padding: 32px;
                background: rgba(8, 20, 54, 0.88);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 28px;
                box-shadow: 0 35px 90px rgba(0,0,0,0.23);
                backdrop-filter: blur(14px);
            }
            .container {
                text-align: center;
            }
            .card-behind {
                display: inline-block;
                padding: 12px 18px;
                border-radius: 18px;
                background: rgba(8, 28, 90, 0.96);
                box-shadow: 0 18px 38px rgba(2,14,55,0.38);
                color: #f8fafc;
                margin-bottom: 18px;
            }
            h1, h2, h3 {
                margin: 0 0 20px;
            }
            h2 {
                color: #dbeafe;
            }
            .section-title {
                grid-column: 1 / -1;
                margin: 0 0 14px;
                font-size: 1.2rem;
                letter-spacing: 0.02em;
            }
            .filters, .summary, .actions, .form-grid {
                display: grid;
                gap: 16px;
            }
            .filters {
                background: rgba(255,255,255,0.08);
                border: 1px solid rgba(255,255,255,0.12);
                padding: 24px;
                border-radius: 22px;
            }
            .filter-row {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 16px;
                align-items: end;
            }
            .filter-group {
                display: flex;
                flex-direction: column;
                text-align: left;
            }
            .filter-group label,
            label {
                margin-bottom: 8px;
                font-weight: 600;
                color: #e2e8f0;
            }
            .filter-group input,
            .filter-group select,
            input,
            select,
            textarea {
                width: 100%;
                padding: 14px 16px;
                border-radius: 16px;
                border: 1px solid rgba(255,255,255,0.14);
                background: rgba(255,255,255,0.96);
                color: #1f2937;
                transition: border-color 0.25s ease, box-shadow 0.25s ease;
            }
            input:focus,
            select:focus,
            textarea:focus {
                outline: none;
                border-color: rgba(96,165,250,0.85);
                box-shadow: 0 0 0 4px rgba(59,130,246,0.12);
            }
            .form-actions,
            .actions {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 14px;
                margin-top: 18px;
            }
            .btn {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                gap: 0.5rem;
                padding: 12px 22px;
                border: none;
                border-radius: 999px;
                cursor: pointer;
                text-decoration: none;
                color: #fff;
                transition: transform 0.2s ease, filter 0.2s ease, background 0.25s ease;
                font-weight: 700;
            }
            .btn:hover {
                transform: translateY(-1px);
                filter: brightness(1.05);
            }
            .btn-primary { background: #2563eb; }
            .btn-primary:hover { background: #1d4ed8; }
            .btn-secondary {
                background: #475569;
                border: 1px solid rgba(255,255,255,0.18);
                color: #eff6ff;
            }
            .btn-secondary:hover {
                background: #334155;
            }
            .btn-danger { background: #ef4444; }
            .btn-danger:hover { background: #dc2626; }
            .btn-small {
                padding: 10px 16px;
                border-radius: 14px;
            }
            .btn-block {
                width: 100%;
            }
            .table-card {
                overflow: hidden;
                border-radius: 24px;
                border: 1px solid rgba(255,255,255,0.08);
                box-shadow: inset 0 0 0 1px rgba(255,255,255,0.02);
            }
            table {
                width: 100%;
                border-collapse: separate;
                border-spacing: 0;
                margin-top: 22px;
                border-radius: 18px;
                overflow: hidden;
                background: rgba(255,255,255,0.04);
            }
            th, td {
                padding: 16px 18px;
                background: rgba(255,255,255,0.06);
                border-bottom: 1px solid rgba(255,255,255,0.08);
                color: #eff6ff;
            }
            th {
                background: rgba(255,255,255,0.12);
                font-weight: 700;
                letter-spacing: 0.03em;
            }
            tr:hover {
                background: rgba(255,255,255,0.08);
            }
            .low-stock {
                background: rgba(248, 113, 113, 0.16);
            }
            .stock-warning {
                padding: 20px;
                border-radius: 22px;
                background: rgba(248, 113, 113, 0.14);
                border: 1px solid rgba(248, 113, 113, 0.18);
                box-shadow: inset 0 0 0 1px rgba(255,255,255,0.05);
                text-align: left;
            }
            .summary {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 18px;
                margin-top: 18px;
            }
            .summary .card {
                padding: 20px;
                border-radius: 24px;
                background: rgba(255,255,255,0.08);
                border: 1px solid rgba(255,255,255,0.12);
                box-shadow: 0 20px 40px rgba(0,0,0,0.12);
                text-align: left;
            }
            .summary .card strong {
                display: block;
                margin-bottom: 12px;
                color: #dbeafe;
            }
            .metric-value,
            .metric-detail {
                margin-top: 12px;
                font-size: 1.35rem;
                color: #e2e8f0;
                line-height: 1.4;
            }
            .empty-row td {
                text-align: center;
                padding: 20px;
            }
            .footer-note {
                margin-top: 24px;
                font-size: 0.95rem;
                color: rgba(226,232,240,0.68);
            }
        </style>
    </head>
    <body>
        <header>
            <h1 class="card-behind">🏆 Loja de Jogos 🏆</h1>
            <nav>
                <a href="{{ url_for('index') }}">Jogos</a>
                <a href="{{ url_for('clientes') }}">Clientes</a>
                
                <a href="{{ url_for('controle_estoque') }}">Estoque</a>
            </nav>
        </header>
        <div class="container">
            <h1 class="card-behind">Atualizar Estoque</h1>
            <form method="post">
                <label>Jogo:</label>
                <input type="text" value="{{ jogo[1] }} ({{ jogo[2] }})" disabled>
                <label for="quantidade">Quantidade Atual:</label>
                <input type="number" id="quantidade" name="quantidade" value="{{ jogo[3] }}" min="0" required>
                <input class="btn btn-primary" type="submit" value="Salvar Quantidade">
                <a class="btn btn-secondary" href="{{ url_for('controle_estoque') }}">Voltar</a>
            </form>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html, jogo=jogo)

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
                font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: radial-gradient(circle at top left, rgba(40, 108, 201, 0.88), transparent 26%),
                            linear-gradient(135deg, #071a3d 0%, #112d5d 45%, #14366f 100%);
                color: #f3f7ff;
                margin: 0;
                padding: 0;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            * {
                box-sizing: border-box;
            }
            header {
                width: 100%;
                background: rgba(5, 18, 52, 0.94);
                padding: 18px 0;
                text-align: center;
                box-shadow: 0 20px 70px rgba(1,16,58,0.34);
                border-bottom: 1px solid rgba(255,255,255,0.08);
                position: sticky;
                top: 0;
                z-index: 10;
            }
            header h1 {
                margin: 0;
                font-size: 2.4rem;
                line-height: 1.05;
                text-shadow: 0 4px 18px rgba(0,0,0,0.35);
            }
            nav {
                margin-top: 14px;
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                gap: 12px;
            }
            nav a {
                color: #fff;
                text-decoration: none;
                padding: 12px 24px;
                background: rgba(255,255,255,0.1);
                border-radius: 999px;
                border: 1px solid rgba(255,255,255,0.14);
                transition: transform 0.25s ease, background 0.25s ease, border-color 0.25s ease;
                font-weight: 600;
            }
            nav a:hover {
                background: rgba(255,255,255,0.18);
                transform: translateY(-1px);
                border-color: rgba(255,255,255,0.22);
            }
            .container, .main-container {
                width: min(1120px, 100%);
                margin: 32px auto 40px;
                padding: 32px;
                background: rgba(8, 20, 54, 0.88);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 28px;
                box-shadow: 0 35px 90px rgba(0,0,0,0.23);
                backdrop-filter: blur(14px);
            }
            .container {
                text-align: center;
            }
            .card-behind {
                display: inline-block;
                padding: 12px 18px;
                border-radius: 18px;
                background: rgba(8, 28, 90, 0.96);
                box-shadow: 0 18px 38px rgba(2,14,55,0.38);
                color: #f8fafc;
                margin-bottom: 18px;
            }
            h1, h2, h3 {
                margin: 0 0 20px;
            }
            h2 {
                color: #dbeafe;
            }
            .section-title {
                grid-column: 1 / -1;
                margin: 0 0 14px;
                font-size: 1.2rem;
                letter-spacing: 0.02em;
            }
            .filters, .summary, .actions, .form-grid {
                display: grid;
                gap: 16px;
            }
            .filters {
                background: rgba(255,255,255,0.08);
                border: 1px solid rgba(255,255,255,0.12);
                padding: 24px;
                border-radius: 22px;
            }
            .filter-row {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 16px;
                align-items: end;
            }
            .filter-group {
                display: flex;
                flex-direction: column;
                text-align: left;
            }
            .filter-group label,
            label {
                margin-bottom: 8px;
                font-weight: 600;
                color: #e2e8f0;
            }
            .filter-group input,
            .filter-group select,
            input,
            select,
            textarea {
                width: 100%;
                padding: 14px 16px;
                border-radius: 16px;
                border: 1px solid rgba(255,255,255,0.14);
                background: rgba(255,255,255,0.96);
                color: #1f2937;
                transition: border-color 0.25s ease, box-shadow 0.25s ease;
            }
            input:focus,
            select:focus,
            textarea:focus {
                outline: none;
                border-color: rgba(96,165,250,0.85);
                box-shadow: 0 0 0 4px rgba(59,130,246,0.12);
            }
            .form-actions,
            .actions {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 14px;
                margin-top: 18px;
            }
            .btn {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                gap: 0.5rem;
                padding: 12px 22px;
                border: none;
                border-radius: 999px;
                cursor: pointer;
                text-decoration: none;
                color: #fff;
                transition: transform 0.2s ease, filter 0.2s ease, background 0.25s ease;
                font-weight: 700;
            }
            .btn:hover {
                transform: translateY(-1px);
                filter: brightness(1.05);
            }
            .btn-primary { background: #2563eb; }
            .btn-primary:hover { background: #1d4ed8; }
            .btn-secondary {
                background: #475569;
                border: 1px solid rgba(255,255,255,0.18);
                color: #eff6ff;
            }
            .btn-secondary:hover {
                background: #334155;
            }
            .btn-danger { background: #ef4444; }
            .btn-danger:hover { background: #dc2626; }
            .btn-small {
                padding: 10px 16px;
                border-radius: 14px;
            }
            .btn-block {
                width: 100%;
            }
            .table-card {
                overflow: hidden;
                border-radius: 24px;
                border: 1px solid rgba(255,255,255,0.08);
                box-shadow: inset 0 0 0 1px rgba(255,255,255,0.02);
            }
            table {
                width: 100%;
                border-collapse: separate;
                border-spacing: 0;
                margin-top: 22px;
                border-radius: 18px;
                overflow: hidden;
                background: rgba(255,255,255,0.04);
            }
            th, td {
                padding: 16px 18px;
                background: rgba(255,255,255,0.06);
                border-bottom: 1px solid rgba(255,255,255,0.08);
                color: #eff6ff;
            }
            th {
                background: rgba(255,255,255,0.12);
                font-weight: 700;
                letter-spacing: 0.03em;
            }
            tr:hover {
                background: rgba(255,255,255,0.08);
            }
            .low-stock {
                background: rgba(248, 113, 113, 0.16);
            }
            .stock-warning {
                padding: 20px;
                border-radius: 22px;
                background: rgba(248, 113, 113, 0.14);
                border: 1px solid rgba(248, 113, 113, 0.18);
                box-shadow: inset 0 0 0 1px rgba(255,255,255,0.05);
                text-align: left;
            }
            .summary {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 18px;
                margin-top: 18px;
            }
            .summary .card {
                padding: 20px;
                border-radius: 24px;
                background: rgba(255,255,255,0.08);
                border: 1px solid rgba(255,255,255,0.12);
                box-shadow: 0 20px 40px rgba(0,0,0,0.12);
                text-align: left;
            }
            .summary .card strong {
                display: block;
                margin-bottom: 12px;
                color: #dbeafe;
            }
            .metric-value,
            .metric-detail {
                margin-top: 12px;
                font-size: 1.35rem;
                color: #e2e8f0;
                line-height: 1.4;
            }
            .empty-row td {
                text-align: center;
                padding: 20px;
            }
            .footer-note {
                margin-top: 24px;
                font-size: 0.95rem;
                color: rgba(226,232,240,0.68);
            }
        </style>
    </head>
    <body>
        <header>
            <h1 class="card-behind">🏆 Loja de Jogos 🏆</h1>
            <nav>
                <a href="{{ url_for('index') }}">Jogos</a>
                <a href="{{ url_for('clientes') }}">Clientes</a>
                
            </nav>
        </header>
        <div class="container">
            <h1 class="card-behind">Cadastrar Novo Jogo</h1>
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
                font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: radial-gradient(circle at top left, rgba(40, 108, 201, 0.88), transparent 26%),
                            linear-gradient(135deg, #071a3d 0%, #112d5d 45%, #14366f 100%);
                color: #f3f7ff;
                margin: 0;
                padding: 0;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            * {
                box-sizing: border-box;
            }
            header {
                width: 100%;
                background: rgba(5, 18, 52, 0.94);
                padding: 18px 0;
                text-align: center;
                box-shadow: 0 20px 70px rgba(1,16,58,0.34);
                border-bottom: 1px solid rgba(255,255,255,0.08);
                position: sticky;
                top: 0;
                z-index: 10;
            }
            header h1 {
                margin: 0;
                font-size: 2.4rem;
                line-height: 1.05;
                text-shadow: 0 4px 18px rgba(0,0,0,0.35);
            }
            nav {
                margin-top: 14px;
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                gap: 12px;
            }
            nav a {
                color: #fff;
                text-decoration: none;
                padding: 12px 24px;
                background: rgba(255,255,255,0.1);
                border-radius: 999px;
                border: 1px solid rgba(255,255,255,0.14);
                transition: transform 0.25s ease, background 0.25s ease, border-color 0.25s ease;
                font-weight: 600;
            }
            nav a:hover {
                background: rgba(255,255,255,0.18);
                transform: translateY(-1px);
                border-color: rgba(255,255,255,0.22);
            }
            .container, .main-container {
                width: min(1120px, 100%);
                margin: 32px auto 40px;
                padding: 32px;
                background: rgba(8, 20, 54, 0.88);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 28px;
                box-shadow: 0 35px 90px rgba(0,0,0,0.23);
                backdrop-filter: blur(14px);
            }
            .container {
                text-align: center;
            }
            .card-behind {
                display: inline-block;
                padding: 12px 18px;
                border-radius: 18px;
                background: rgba(8, 28, 90, 0.96);
                box-shadow: 0 18px 38px rgba(2,14,55,0.38);
                color: #f8fafc;
                margin-bottom: 18px;
            }
            h1, h2, h3 {
                margin: 0 0 20px;
            }
            h2 {
                color: #dbeafe;
            }
            .section-title {
                grid-column: 1 / -1;
                margin: 0 0 14px;
                font-size: 1.2rem;
                letter-spacing: 0.02em;
            }
            .filters, .summary, .actions, .form-grid {
                display: grid;
                gap: 16px;
            }
            .filters {
                background: rgba(255,255,255,0.08);
                border: 1px solid rgba(255,255,255,0.12);
                padding: 24px;
                border-radius: 22px;
            }
            .filter-row {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 16px;
                align-items: end;
            }
            .filter-group {
                display: flex;
                flex-direction: column;
                text-align: left;
            }
            .filter-group label,
            label {
                margin-bottom: 8px;
                font-weight: 600;
                color: #e2e8f0;
            }
            .filter-group input,
            .filter-group select,
            input,
            select,
            textarea {
                width: 100%;
                padding: 14px 16px;
                border-radius: 16px;
                border: 1px solid rgba(255,255,255,0.14);
                background: rgba(255,255,255,0.96);
                color: #1f2937;
                transition: border-color 0.25s ease, box-shadow 0.25s ease;
            }
            input:focus,
            select:focus,
            textarea:focus {
                outline: none;
                border-color: rgba(96,165,250,0.85);
                box-shadow: 0 0 0 4px rgba(59,130,246,0.12);
            }
            .form-actions,
            .actions {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 14px;
                margin-top: 18px;
            }
            .btn {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                gap: 0.5rem;
                padding: 12px 22px;
                border: none;
                border-radius: 999px;
                cursor: pointer;
                text-decoration: none;
                color: #fff;
                transition: transform 0.2s ease, filter 0.2s ease, background 0.25s ease;
                font-weight: 700;
            }
            .btn:hover {
                transform: translateY(-1px);
                filter: brightness(1.05);
            }
            .btn-primary { background: #2563eb; }
            .btn-primary:hover { background: #1d4ed8; }
            .btn-secondary {
                background: #475569;
                border: 1px solid rgba(255,255,255,0.18);
                color: #eff6ff;
            }
            .btn-secondary:hover {
                background: #334155;
            }
            .btn-danger { background: #ef4444; }
            .btn-danger:hover { background: #dc2626; }
            .btn-small {
                padding: 10px 16px;
                border-radius: 14px;
            }
            .btn-block {
                width: 100%;
            }
            .table-card {
                overflow: hidden;
                border-radius: 24px;
                border: 1px solid rgba(255,255,255,0.08);
                box-shadow: inset 0 0 0 1px rgba(255,255,255,0.02);
            }
            table {
                width: 100%;
                border-collapse: separate;
                border-spacing: 0;
                margin-top: 22px;
                border-radius: 18px;
                overflow: hidden;
                background: rgba(255,255,255,0.04);
            }
            th, td {
                padding: 16px 18px;
                background: rgba(255,255,255,0.06);
                border-bottom: 1px solid rgba(255,255,255,0.08);
                color: #eff6ff;
            }
            th {
                background: rgba(255,255,255,0.12);
                font-weight: 700;
                letter-spacing: 0.03em;
            }
            tr:hover {
                background: rgba(255,255,255,0.08);
            }
            .low-stock {
                background: rgba(248, 113, 113, 0.16);
            }
            .stock-warning {
                padding: 20px;
                border-radius: 22px;
                background: rgba(248, 113, 113, 0.14);
                border: 1px solid rgba(248, 113, 113, 0.18);
                box-shadow: inset 0 0 0 1px rgba(255,255,255,0.05);
                text-align: left;
            }
            .summary {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 18px;
                margin-top: 18px;
            }
            .summary .card {
                padding: 20px;
                border-radius: 24px;
                background: rgba(255,255,255,0.08);
                border: 1px solid rgba(255,255,255,0.12);
                box-shadow: 0 20px 40px rgba(0,0,0,0.12);
                text-align: left;
            }
            .summary .card strong {
                display: block;
                margin-bottom: 12px;
                color: #dbeafe;
            }
            .metric-value,
            .metric-detail {
                margin-top: 12px;
                font-size: 1.35rem;
                color: #e2e8f0;
                line-height: 1.4;
            }
            .empty-row td {
                text-align: center;
                padding: 20px;
            }
            .footer-note {
                margin-top: 24px;
                font-size: 0.95rem;
                color: rgba(226,232,240,0.68);
            }
        </style>
    </head>
    <body>
        <header>
            <h1 class="card-behind">🏆 Loja de Jogos 🏆</h1>
            <nav>
                <a href="{{ url_for('index') }}">Jogos</a>
                <a href="{{ url_for('clientes') }}">Clientes</a>
                
            </nav>
        </header>
        <div class="container">
            <h1 class="card-behind">Clientes Cadastrados</h1>
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
                font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: radial-gradient(circle at top left, rgba(40, 108, 201, 0.88), transparent 26%),
                            linear-gradient(135deg, #071a3d 0%, #112d5d 45%, #14366f 100%);
                color: #f3f7ff;
                margin: 0;
                padding: 0;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            * {
                box-sizing: border-box;
            }
            header {
                width: 100%;
                background: rgba(5, 18, 52, 0.94);
                padding: 18px 0;
                text-align: center;
                box-shadow: 0 20px 70px rgba(1,16,58,0.34);
                border-bottom: 1px solid rgba(255,255,255,0.08);
                position: sticky;
                top: 0;
                z-index: 10;
            }
            header h1 {
                margin: 0;
                font-size: 2.4rem;
                line-height: 1.05;
                text-shadow: 0 4px 18px rgba(0,0,0,0.35);
            }
            nav {
                margin-top: 14px;
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                gap: 12px;
            }
            nav a {
                color: #fff;
                text-decoration: none;
                padding: 12px 24px;
                background: rgba(255,255,255,0.1);
                border-radius: 999px;
                border: 1px solid rgba(255,255,255,0.14);
                transition: transform 0.25s ease, background 0.25s ease, border-color 0.25s ease;
                font-weight: 600;
            }
            nav a:hover {
                background: rgba(255,255,255,0.18);
                transform: translateY(-1px);
                border-color: rgba(255,255,255,0.22);
            }
            .container, .main-container {
                width: min(1120px, 100%);
                margin: 32px auto 40px;
                padding: 32px;
                background: rgba(8, 20, 54, 0.88);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 28px;
                box-shadow: 0 35px 90px rgba(0,0,0,0.23);
                backdrop-filter: blur(14px);
            }
            .container {
                text-align: center;
            }
            .card-behind {
                display: inline-block;
                padding: 12px 18px;
                border-radius: 18px;
                background: rgba(8, 28, 90, 0.96);
                box-shadow: 0 18px 38px rgba(2,14,55,0.38);
                color: #f8fafc;
                margin-bottom: 18px;
            }
            h1, h2, h3 {
                margin: 0 0 20px;
            }
            h2 {
                color: #dbeafe;
            }
            .section-title {
                grid-column: 1 / -1;
                margin: 0 0 14px;
                font-size: 1.2rem;
                letter-spacing: 0.02em;
            }
            .filters, .summary, .actions, .form-grid {
                display: grid;
                gap: 16px;
            }
            .filters {
                background: rgba(255,255,255,0.08);
                border: 1px solid rgba(255,255,255,0.12);
                padding: 24px;
                border-radius: 22px;
            }
            .filter-row {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 16px;
                align-items: end;
            }
            .filter-group {
                display: flex;
                flex-direction: column;
                text-align: left;
            }
            .filter-group label,
            label {
                margin-bottom: 8px;
                font-weight: 600;
                color: #e2e8f0;
            }
            .filter-group input,
            .filter-group select,
            input,
            select,
            textarea {
                width: 100%;
                padding: 14px 16px;
                border-radius: 16px;
                border: 1px solid rgba(255,255,255,0.14);
                background: rgba(255,255,255,0.96);
                color: #1f2937;
                transition: border-color 0.25s ease, box-shadow 0.25s ease;
            }
            input:focus,
            select:focus,
            textarea:focus {
                outline: none;
                border-color: rgba(96,165,250,0.85);
                box-shadow: 0 0 0 4px rgba(59,130,246,0.12);
            }
            .form-actions,
            .actions {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 14px;
                margin-top: 18px;
            }
            .btn {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                gap: 0.5rem;
                padding: 12px 22px;
                border: none;
                border-radius: 999px;
                cursor: pointer;
                text-decoration: none;
                color: #fff;
                transition: transform 0.2s ease, filter 0.2s ease, background 0.25s ease;
                font-weight: 700;
            }
            .btn:hover {
                transform: translateY(-1px);
                filter: brightness(1.05);
            }
            .btn-primary { background: #2563eb; }
            .btn-primary:hover { background: #1d4ed8; }
            .btn-secondary {
                background: #475569;
                border: 1px solid rgba(255,255,255,0.18);
                color: #eff6ff;
            }
            .btn-secondary:hover {
                background: #334155;
            }
            .btn-danger { background: #ef4444; }
            .btn-danger:hover { background: #dc2626; }
            .btn-small {
                padding: 10px 16px;
                border-radius: 14px;
            }
            .btn-block {
                width: 100%;
            }
            .table-card {
                overflow: hidden;
                border-radius: 24px;
                border: 1px solid rgba(255,255,255,0.08);
                box-shadow: inset 0 0 0 1px rgba(255,255,255,0.02);
            }
            table {
                width: 100%;
                border-collapse: separate;
                border-spacing: 0;
                margin-top: 22px;
                border-radius: 18px;
                overflow: hidden;
                background: rgba(255,255,255,0.04);
            }
            th, td {
                padding: 16px 18px;
                background: rgba(255,255,255,0.06);
                border-bottom: 1px solid rgba(255,255,255,0.08);
                color: #eff6ff;
            }
            th {
                background: rgba(255,255,255,0.12);
                font-weight: 700;
                letter-spacing: 0.03em;
            }
            tr:hover {
                background: rgba(255,255,255,0.08);
            }
            .low-stock {
                background: rgba(248, 113, 113, 0.16);
            }
            .stock-warning {
                padding: 20px;
                border-radius: 22px;
                background: rgba(248, 113, 113, 0.14);
                border: 1px solid rgba(248, 113, 113, 0.18);
                box-shadow: inset 0 0 0 1px rgba(255,255,255,0.05);
                text-align: left;
            }
            .summary {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 18px;
                margin-top: 18px;
            }
            .summary .card {
                padding: 20px;
                border-radius: 24px;
                background: rgba(255,255,255,0.08);
                border: 1px solid rgba(255,255,255,0.12);
                box-shadow: 0 20px 40px rgba(0,0,0,0.12);
                text-align: left;
            }
            .summary .card strong {
                display: block;
                margin-bottom: 12px;
                color: #dbeafe;
            }
            .metric-value,
            .metric-detail {
                margin-top: 12px;
                font-size: 1.35rem;
                color: #e2e8f0;
                line-height: 1.4;
            }
            .empty-row td {
                text-align: center;
                padding: 20px;
            }
            .footer-note {
                margin-top: 24px;
                font-size: 0.95rem;
                color: rgba(226,232,240,0.68);
            }
        </style>
    </head>
    <body>
        <header>
            <h1 class="card-behind">🏆 Loja de Jogos 🏆</h1>
            <nav>
                <a href="{{ url_for('index') }}">Jogos</a>
                <a href="{{ url_for('clientes') }}">Clientes</a>
                
            </nav>
        </header>
        <div class="container">
            <h1 class="card-behind">Cadastrar Novo Cliente</h1>
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
    # Detailed sales list
    cursor.execute('''
        SELECT v.id, c.nome, j.nome, v.quantidade, v.data
        FROM vendas v
        JOIN clientes c ON v.cliente_id = c.id
        JOIN jogos j ON v.jogo_id = j.id
        ORDER BY v.data DESC
    ''')
    vendas_list = cursor.fetchall()

    # Total items sold overall
    cursor.execute('SELECT SUM(quantidade) FROM vendas')
    total_items_row = cursor.fetchone()
    total_items = total_items_row[0] if total_items_row and total_items_row[0] is not None else 0

    # Total number of vendas (transactions)
    cursor.execute('SELECT COUNT(*) FROM vendas')
    total_vendas = cursor.fetchone()[0]

    # Aggregated history: total sold per jogo
    cursor.execute('''
        SELECT j.id, j.nome, j.plataforma, SUM(v.quantidade) as total_vendido
        FROM vendas v
        JOIN jogos j ON v.jogo_id = j.id
        GROUP BY j.id
        ORDER BY total_vendido DESC
    ''')
    vendas_por_jogo = cursor.fetchall()

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
                font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: radial-gradient(circle at top left, rgba(40, 108, 201, 0.88), transparent 26%),
                            linear-gradient(135deg, #071a3d 0%, #112d5d 45%, #14366f 100%);
                color: #f3f7ff;
                margin: 0;
                padding: 0;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            * {
                box-sizing: border-box;
            }
            header {
                width: 100%;
                background: rgba(5, 18, 52, 0.94);
                padding: 18px 0;
                text-align: center;
                box-shadow: 0 20px 70px rgba(1,16,58,0.34);
                border-bottom: 1px solid rgba(255,255,255,0.08);
                position: sticky;
                top: 0;
                z-index: 10;
            }
            header h1 {
                margin: 0;
                font-size: 2.4rem;
                line-height: 1.05;
                text-shadow: 0 4px 18px rgba(0,0,0,0.35);
            }
            nav {
                margin-top: 14px;
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                gap: 12px;
            }
            nav a {
                color: #fff;
                text-decoration: none;
                padding: 12px 24px;
                background: rgba(255,255,255,0.1);
                border-radius: 999px;
                border: 1px solid rgba(255,255,255,0.14);
                transition: transform 0.25s ease, background 0.25s ease, border-color 0.25s ease;
                font-weight: 600;
            }
            nav a:hover {
                background: rgba(255,255,255,0.18);
                transform: translateY(-1px);
                border-color: rgba(255,255,255,0.22);
            }
            .container, .main-container {
                width: min(1120px, 100%);
                margin: 32px auto 40px;
                padding: 32px;
                background: rgba(8, 20, 54, 0.88);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 28px;
                box-shadow: 0 35px 90px rgba(0,0,0,0.23);
                backdrop-filter: blur(14px);
            }
            .container {
                text-align: center;
            }
            .card-behind {
                display: inline-block;
                padding: 12px 18px;
                border-radius: 18px;
                background: rgba(8, 28, 90, 0.96);
                box-shadow: 0 18px 38px rgba(2,14,55,0.38);
                color: #f8fafc;
                margin-bottom: 18px;
            }
            h1, h2, h3 {
                margin: 0 0 20px;
            }
            h2 {
                color: #dbeafe;
            }
            .section-title {
                grid-column: 1 / -1;
                margin: 0 0 14px;
                font-size: 1.2rem;
                letter-spacing: 0.02em;
            }
            .filters, .summary, .actions, .form-grid {
                display: grid;
                gap: 16px;
            }
            .filters {
                background: rgba(255,255,255,0.08);
                border: 1px solid rgba(255,255,255,0.12);
                padding: 24px;
                border-radius: 22px;
            }
            .filter-row {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 16px;
                align-items: end;
            }
            .filter-group {
                display: flex;
                flex-direction: column;
                text-align: left;
            }
            .filter-group label,
            label {
                margin-bottom: 8px;
                font-weight: 600;
                color: #e2e8f0;
            }
            .filter-group input,
            .filter-group select,
            input,
            select,
            textarea {
                width: 100%;
                padding: 14px 16px;
                border-radius: 16px;
                border: 1px solid rgba(255,255,255,0.14);
                background: rgba(255,255,255,0.96);
                color: #1f2937;
                transition: border-color 0.25s ease, box-shadow 0.25s ease;
            }
            input:focus,
            select:focus,
            textarea:focus {
                outline: none;
                border-color: rgba(96,165,250,0.85);
                box-shadow: 0 0 0 4px rgba(59,130,246,0.12);
            }
            .form-actions,
            .actions {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 14px;
                margin-top: 18px;
            }
            .btn {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                gap: 0.5rem;
                padding: 12px 22px;
                border: none;
                border-radius: 999px;
                cursor: pointer;
                text-decoration: none;
                color: #fff;
                transition: transform 0.2s ease, filter 0.2s ease, background 0.25s ease;
                font-weight: 700;
            }
            .btn:hover {
                transform: translateY(-1px);
                filter: brightness(1.05);
            }
            .btn-primary { background: #2563eb; }
            .btn-primary:hover { background: #1d4ed8; }
            .btn-secondary {
                background: #475569;
                border: 1px solid rgba(255,255,255,0.18);
                color: #eff6ff;
            }
            .btn-secondary:hover {
                background: #334155;
            }
            .btn-danger { background: #ef4444; }
            .btn-danger:hover { background: #dc2626; }
            .btn-small {
                padding: 10px 16px;
                border-radius: 14px;
            }
            .btn-block {
                width: 100%;
            }
            .table-card {
                overflow: hidden;
                border-radius: 24px;
                border: 1px solid rgba(255,255,255,0.08);
                box-shadow: inset 0 0 0 1px rgba(255,255,255,0.02);
            }
            table {
                width: 100%;
                border-collapse: separate;
                border-spacing: 0;
                margin-top: 22px;
                border-radius: 18px;
                overflow: hidden;
                background: rgba(255,255,255,0.04);
            }
            th, td {
                padding: 16px 18px;
                background: rgba(255,255,255,0.06);
                border-bottom: 1px solid rgba(255,255,255,0.08);
                color: #eff6ff;
            }
            th {
                background: rgba(255,255,255,0.12);
                font-weight: 700;
                letter-spacing: 0.03em;
            }
            tr:hover {
                background: rgba(255,255,255,0.08);
            }
            .low-stock {
                background: rgba(248, 113, 113, 0.16);
            }
            .stock-warning {
                padding: 20px;
                border-radius: 22px;
                background: rgba(248, 113, 113, 0.14);
                border: 1px solid rgba(248, 113, 113, 0.18);
                box-shadow: inset 0 0 0 1px rgba(255,255,255,0.05);
                text-align: left;
            }
            .summary {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 18px;
                margin-top: 18px;
            }
            .summary .card {
                padding: 20px;
                border-radius: 24px;
                background: rgba(255,255,255,0.08);
                border: 1px solid rgba(255,255,255,0.12);
                box-shadow: 0 20px 40px rgba(0,0,0,0.12);
                text-align: left;
            }
            .summary .card strong {
                display: block;
                margin-bottom: 12px;
                color: #dbeafe;
            }
            .metric-value,
            .metric-detail {
                margin-top: 12px;
                font-size: 1.35rem;
                color: #e2e8f0;
                line-height: 1.4;
            }
            .empty-row td {
                text-align: center;
                padding: 20px;
            }
            .footer-note {
                margin-top: 24px;
                font-size: 0.95rem;
                color: rgba(226,232,240,0.68);
            }
        </style>
    </head>
    <body>
        <header>
            <h1 class="card-behind">🏆 Loja de Jogos 🏆</h1>
            <nav>
                <a href="{{ url_for('index') }}">Jogos</a>
                <a href="{{ url_for('clientes') }}">Clientes</a>
                
            </nav>
        </header>
        <div class="container">
            <h1 class="card-behind">Vendas Registradas</h1>
            <a class="btn btn-primary" href="{{ url_for('registrar_venda') }}">Registrar Nova Venda</a>
            
            <div class="summary">
                <div class="card">
                    <strong>Total de transações:</strong>
                    <div class="metric-value">{{ total_vendas }}</div>
                </div>
                <div class="card">
                    <strong>Total de itens vendidos:</strong>
                    <div class="metric-value">{{ total_items }}</div>
                </div>
                <div class="card">
                    <strong>Jogos com maiores vendas:</strong>
                    <div class="metric-detail">
                        {% for jogo in vendas_por_jogo[:3] %}
                            <div>{{ jogo[1] }} ({{ jogo[3] }} itens)</div>
                        {% else %}
                            <div>Nenhum registro</div>
                        {% endfor %}
                    </div>
                </div>
            </div>

            <h2>Histórico completo de vendas</h2>
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

            <h2 class="section-title">Resumo por jogo</h2>
            <table>
                <tr><th>ID</th><th>Nome</th><th>Plataforma</th><th>Total Vendido</th></tr>
                {% for jogo in vendas_por_jogo %}
                <tr>
                    <td>{{ jogo[0] }}</td>
                    <td>{{ jogo[1] }}</td>
                    <td>{{ jogo[2] }}</td>
                    <td>{{ jogo[3] }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html, vendas_list=vendas_list, total_items=total_items, total_vendas=total_vendas, vendas_por_jogo=vendas_por_jogo)

@app.route('/relatorio')
def relatorio():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    mes_atual = datetime.now().strftime('%Y-%m')
    cursor.execute('SELECT SUM(quantidade) FROM vendas WHERE strftime("%Y-%m", data) = ?', (mes_atual,))
    total_vendidos_mes = cursor.fetchone()[0] or 0
    cursor.execute('SELECT COUNT(*) FROM vendas WHERE strftime("%Y-%m", data) = ?', (mes_atual,))
    total_vendas_mes = cursor.fetchone()[0] or 0
    cursor.execute('SELECT SUM(quantidade) FROM jogos')
    total_estoque = cursor.fetchone()[0] or 0
    cursor.execute('''
        SELECT j.id, j.nome, j.plataforma, SUM(v.quantidade) as total_vendido
        FROM vendas v
        JOIN jogos j ON v.jogo_id = j.id
        WHERE strftime("%Y-%m", v.data) = ?
        GROUP BY j.id
        ORDER BY total_vendido DESC
        LIMIT 5
    ''', (mes_atual,))
    top_jogos_mes = cursor.fetchall()
    conn.close()
    html = '''
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Loja de Jogos - Relatório</title>
        <style>
            body {
                font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: radial-gradient(circle at top left, rgba(40, 108, 201, 0.88), transparent 26%),
                            linear-gradient(135deg, #071a3d 0%, #112d5d 45%, #14366f 100%);
                color: #f3f7ff;
                margin: 0;
                padding: 0;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            * {
                box-sizing: border-box;
            }
            header {
                width: 100%;
                background: rgba(5, 18, 52, 0.94);
                padding: 18px 0;
                text-align: center;
                box-shadow: 0 20px 70px rgba(1,16,58,0.34);
                border-bottom: 1px solid rgba(255,255,255,0.08);
                position: sticky;
                top: 0;
                z-index: 10;
            }
            header h1 {
                margin: 0;
                font-size: 2.4rem;
                line-height: 1.05;
                text-shadow: 0 4px 18px rgba(0,0,0,0.35);
            }
            nav {
                margin-top: 14px;
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                gap: 12px;
            }
            nav a {
                color: #fff;
                text-decoration: none;
                padding: 12px 24px;
                background: rgba(255,255,255,0.1);
                border-radius: 999px;
                border: 1px solid rgba(255,255,255,0.14);
                transition: transform 0.25s ease, background 0.25s ease, border-color 0.25s ease;
                font-weight: 600;
            }
            nav a:hover {
                background: rgba(255,255,255,0.18);
                transform: translateY(-1px);
                border-color: rgba(255,255,255,0.22);
            }
            .container {
                width: min(1120px, 100%);
                margin: 32px auto 40px;
                padding: 32px;
                background: rgba(8, 20, 54, 0.88);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 28px;
                box-shadow: 0 35px 90px rgba(0,0,0,0.23);
                backdrop-filter: blur(14px);
                text-align: center;
            }
            .card-behind {
                display: inline-block;
                padding: 12px 18px;
                border-radius: 18px;
                background: rgba(8, 28, 90, 0.96);
                box-shadow: 0 18px 38px rgba(2,14,55,0.38);
                color: #f8fafc;
                margin-bottom: 18px;
            }
            .summary {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
                gap: 18px;
                margin-top: 24px;
                text-align: left;
            }
            .card {
                padding: 22px;
                border-radius: 24px;
                background: rgba(255,255,255,0.08);
                border: 1px solid rgba(255,255,255,0.12);
                box-shadow: 0 20px 40px rgba(0,0,0,0.12);
            }
            .card strong {
                display: block;
                margin-bottom: 12px;
                color: #dbeafe;
            }
            .metric-value {
                font-size: 2rem;
                color: #e2e8f0;
                line-height: 1.2;
            }
            .metric-detail {
                margin-top: 12px;
                color: #cbd5e1;
                line-height: 1.5;
            }
            table {
                width: 100%;
                border-collapse: separate;
                border-spacing: 0;
                margin-top: 22px;
                border-radius: 18px;
                overflow: hidden;
                background: rgba(255,255,255,0.04);
            }
            th, td {
                padding: 16px 18px;
                background: rgba(255,255,255,0.06);
                border-bottom: 1px solid rgba(255,255,255,0.08);
                color: #eff6ff;
            }
            th {
                background: rgba(255,255,255,0.12);
                font-weight: 700;
            }
            tr:hover {
                background: rgba(255,255,255,0.08);
            }
            .btn {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                padding: 12px 22px;
                border-radius: 999px;
                border: none;
                cursor: pointer;
                text-decoration: none;
                color: #fff;
                transition: transform 0.2s ease, filter 0.2s ease, background 0.25s ease;
                font-weight: 700;
            }
            .btn:hover { transform: translateY(-1px); }
            .btn-primary { background: #2563eb; }
            .btn-primary:hover { background: #1d4ed8; }
            .btn-secondary {
                background: #475569;
                border: 1px solid rgba(255,255,255,0.18);
                color: #eff6ff;
            }
            .btn-secondary:hover {
                background: #334155;
            }
        </style>
    </head>
    <body>
        <header>
            <h1 class="card-behind">📊 Relatório Simples</h1>
            <nav>
                <a href="{{ url_for('admin_home') }}">Admin</a>
                <a href="{{ url_for('user_home') }}">Usuário</a>
            </nav>
        </header>
        <div class="container">
            <h1 class="card-behind">Resumo do Mês Atual</h1>
            <div class="summary">
                <div class="card">
                    <strong>Total vendido no mês</strong>
                    <div class="metric-value">{{ total_vendidos_mes }}</div>
                    <div class="metric-detail">Unidades vendidas em {{ mes_atual }}</div>
                </div>
                <div class="card">
                    <strong>Total em estoque</strong>
                    <div class="metric-value">{{ total_estoque }}</div>
                    <div class="metric-detail">Soma de todos os jogos cadastrados</div>
                </div>
                <div class="card">
                    <strong>Transações no mês</strong>
                    <div class="metric-value">{{ total_vendas_mes }}</div>
                    <div class="metric-detail">Vendas registradas em {{ mes_atual }}</div>
                </div>
            </div>

            <h2 class="section-title">Jogos mais vendidos no mês</h2>
            <table>
                <tr><th>Nome</th><th>Plataforma</th><th>Total vendido</th></tr>
                {% if top_jogos_mes %}
                    {% for jogo in top_jogos_mes %}
                    <tr>
                        <td>{{ jogo[1] }}</td>
                        <td>{{ jogo[2] }}</td>
                        <td>{{ jogo[3] }}</td>
                    </tr>
                    {% endfor %}
                {% else %}
                    <tr><td colspan="3" style="text-align:center;">Nenhuma venda registrada neste mês</td></tr>
                {% endif %}
            </table>

            <a class="btn btn-secondary" href="{{ url_for('admin_home') }}">Voltar ao Admin</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html, total_vendidos_mes=total_vendidos_mes, total_estoque=total_estoque, total_vendas_mes=total_vendas_mes, top_jogos_mes=top_jogos_mes, mes_atual=mes_atual)

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
                font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: radial-gradient(circle at top left, rgba(40, 108, 201, 0.88), transparent 26%),
                            linear-gradient(135deg, #071a3d 0%, #112d5d 45%, #14366f 100%);
                color: #f3f7ff;
                margin: 0;
                padding: 0;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            * {
                box-sizing: border-box;
            }
            header {
                width: 100%;
                background: rgba(5, 18, 52, 0.94);
                padding: 18px 0;
                text-align: center;
                box-shadow: 0 20px 70px rgba(1,16,58,0.34);
                border-bottom: 1px solid rgba(255,255,255,0.08);
                position: sticky;
                top: 0;
                z-index: 10;
            }
            header h1 {
                margin: 0;
                font-size: 2.4rem;
                line-height: 1.05;
                text-shadow: 0 4px 18px rgba(0,0,0,0.35);
            }
            nav {
                margin-top: 14px;
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                gap: 12px;
            }
            nav a {
                color: #fff;
                text-decoration: none;
                padding: 12px 24px;
                background: rgba(255,255,255,0.1);
                border-radius: 999px;
                border: 1px solid rgba(255,255,255,0.14);
                transition: transform 0.25s ease, background 0.25s ease, border-color 0.25s ease;
                font-weight: 600;
            }
            nav a:hover {
                background: rgba(255,255,255,0.18);
                transform: translateY(-1px);
                border-color: rgba(255,255,255,0.22);
            }
            .container, .main-container {
                width: min(1120px, 100%);
                margin: 32px auto 40px;
                padding: 32px;
                background: rgba(8, 20, 54, 0.88);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 28px;
                box-shadow: 0 35px 90px rgba(0,0,0,0.23);
                backdrop-filter: blur(14px);
            }
            .container {
                text-align: center;
            }
            .card-behind {
                display: inline-block;
                padding: 12px 18px;
                border-radius: 18px;
                background: rgba(8, 28, 90, 0.96);
                box-shadow: 0 18px 38px rgba(2,14,55,0.38);
                color: #f8fafc;
                margin-bottom: 18px;
            }
            h1, h2, h3 {
                margin: 0 0 20px;
            }
            h2 {
                color: #dbeafe;
            }
            .section-title {
                grid-column: 1 / -1;
                margin: 0 0 14px;
                font-size: 1.2rem;
                letter-spacing: 0.02em;
            }
            .filters, .summary, .actions, .form-grid {
                display: grid;
                gap: 16px;
            }
            .filters {
                background: rgba(255,255,255,0.08);
                border: 1px solid rgba(255,255,255,0.12);
                padding: 24px;
                border-radius: 22px;
            }
            .filter-row {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 16px;
                align-items: end;
            }
            .filter-group {
                display: flex;
                flex-direction: column;
                text-align: left;
            }
            .filter-group label,
            label {
                margin-bottom: 8px;
                font-weight: 600;
                color: #e2e8f0;
            }
            .filter-group input,
            .filter-group select,
            input,
            select,
            textarea {
                width: 100%;
                padding: 14px 16px;
                border-radius: 16px;
                border: 1px solid rgba(255,255,255,0.14);
                background: rgba(255,255,255,0.96);
                color: #1f2937;
                transition: border-color 0.25s ease, box-shadow 0.25s ease;
            }
            input:focus,
            select:focus,
            textarea:focus {
                outline: none;
                border-color: rgba(96,165,250,0.85);
                box-shadow: 0 0 0 4px rgba(59,130,246,0.12);
            }
            .form-actions,
            .actions {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 14px;
                margin-top: 18px;
            }
            .btn {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                gap: 0.5rem;
                padding: 12px 22px;
                border: none;
                border-radius: 999px;
                cursor: pointer;
                text-decoration: none;
                color: #fff;
                transition: transform 0.2s ease, filter 0.2s ease, background 0.25s ease;
                font-weight: 700;
            }
            .btn:hover {
                transform: translateY(-1px);
                filter: brightness(1.05);
            }
            .btn-primary { background: #2563eb; }
            .btn-primary:hover { background: #1d4ed8; }
            .btn-secondary {
                background: #475569;
                border: 1px solid rgba(255,255,255,0.18);
                color: #eff6ff;
            }
            .btn-secondary:hover {
                background: #334155;
            }
            .btn-danger { background: #ef4444; }
            .btn-danger:hover { background: #dc2626; }
            .btn-small {
                padding: 10px 16px;
                border-radius: 14px;
            }
            .btn-block {
                width: 100%;
            }
            .table-card {
                overflow: hidden;
                border-radius: 24px;
                border: 1px solid rgba(255,255,255,0.08);
                box-shadow: inset 0 0 0 1px rgba(255,255,255,0.02);
            }
            table {
                width: 100%;
                border-collapse: separate;
                border-spacing: 0;
                margin-top: 22px;
                border-radius: 18px;
                overflow: hidden;
                background: rgba(255,255,255,0.04);
            }
            th, td {
                padding: 16px 18px;
                background: rgba(255,255,255,0.06);
                border-bottom: 1px solid rgba(255,255,255,0.08);
                color: #eff6ff;
            }
            th {
                background: rgba(255,255,255,0.12);
                font-weight: 700;
                letter-spacing: 0.03em;
            }
            tr:hover {
                background: rgba(255,255,255,0.08);
            }
            .low-stock {
                background: rgba(248, 113, 113, 0.16);
            }
            .stock-warning {
                padding: 20px;
                border-radius: 22px;
                background: rgba(248, 113, 113, 0.14);
                border: 1px solid rgba(248, 113, 113, 0.18);
                box-shadow: inset 0 0 0 1px rgba(255,255,255,0.05);
                text-align: left;
            }
            .summary {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 18px;
                margin-top: 18px;
            }
            .summary .card {
                padding: 20px;
                border-radius: 24px;
                background: rgba(255,255,255,0.08);
                border: 1px solid rgba(255,255,255,0.12);
                box-shadow: 0 20px 40px rgba(0,0,0,0.12);
                text-align: left;
            }
            .summary .card strong {
                display: block;
                margin-bottom: 12px;
                color: #dbeafe;
            }
            .metric-value,
            .metric-detail {
                margin-top: 12px;
                font-size: 1.35rem;
                color: #e2e8f0;
                line-height: 1.4;
            }
            .empty-row td {
                text-align: center;
                padding: 20px;
            }
            .footer-note {
                margin-top: 24px;
                font-size: 0.95rem;
                color: rgba(226,232,240,0.68);
            }
        </style>
    </head>
    <body>
        <header>
            <h1 class="card-behind">🏆 Loja de Jogos 🏆</h1>
            <nav>
                <a href="{{ url_for('index') }}">Jogos</a>
                <a href="{{ url_for('clientes') }}">Clientes</a>
                
            </nav>
        </header>
        <div class="container">
            <h1 class="card-behind">Registrar Venda</h1>
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
                
                <div class="form-actions">
                    <input class="btn btn-primary" type="submit" value="Registrar">
                    <a class="btn btn-secondary" href="{{ url_for('vendas') }}">Voltar</a>
                </div>
            </form>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html, clientes=clientes, jogos=jogos)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

# =============================================================================
# CÓDIGO VISUAL PARA MYSQL (APENAS PARA VISUALIZAÇÃO - NÃO EXECUTA)
# Este bloco mostra como seria o código se usasse MySQL em vez de SQLite
# Para usar MySQL, descomente este bloco e comente o código SQLite acima
# Instale: pip install pymysql
# =============================================================================

# import pymysql  # Descomente para usar MySQL

# DATABASE_CONFIG = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': 'sua_senha',
#     'database': 'loja_db',
#     'charset': 'utf8mb4'
# }

# def init_db_mysql():
#     conn = pymysql.connect(**DATABASE_CONFIG)
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS jogos (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             nome VARCHAR(255) NOT NULL,
#             preco DECIMAL(10,2) NOT NULL,
#             plataforma VARCHAR(100) NOT NULL,
#             quantidade INT NOT NULL
#         )
#     ''')
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS clientes (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             nome VARCHAR(255) NOT NULL,
#             email VARCHAR(255) NOT NULL,
#             telefone VARCHAR(20) NOT NULL
#         )
#     ''')
#     conn.commit()
#     conn.close()

# @app.route('/')
# def index_mysql():
#     conn = pymysql.connect(**DATABASE_CONFIG)
#     cursor = conn.cursor()
#     cursor.execute('SELECT id, nome, preco, plataforma, quantidade FROM jogos')
#     jogos = cursor.fetchall()
#     conn.close()
#     # ... resto do HTML igual ao SQLite

# @app.route('/clientes')
# def clientes_mysql():
#     conn = pymysql.connect(**DATABASE_CONFIG)
#     cursor = conn.cursor()
#     cursor.execute('SELECT id, nome, email, telefone FROM clientes')
#     clientes = cursor.fetchall()
#     conn.close()
#     # ... resto do HTML igual ao SQLite

# # Para rodar com MySQL, substitua init_db() por init_db_mysql()
# # if __name__ == '__main__':
# #     init_db_mysql()
# #     app.run(debug=True)

# =============================================================================
# FIM DO CÓDIGO VISUAL MYSQL
# =============================================================================
