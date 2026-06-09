#!/usr/bin/env python3
"""
Script para popular o banco de dados com dados de exemplo.
Execute: python seed.py
"""

import sqlite3
from datetime import datetime, timedelta
import random

DATABASE = 'LojaDB.db'

def seed_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Limpar dados existentes (opcional - comentar se quiser preservar)
    # cursor.execute('DELETE FROM vendas')
    # cursor.execute('DELETE FROM clientes')
    # cursor.execute('DELETE FROM jogos')
    
    # Inserir jogos
    jogos = [
        ('The Legend of Zelda: Breath of the Wild', 299.99, 'Nintendo Switch', 15),
        ('Elden Ring', 249.99, 'PlayStation 5', 8),
        ('Starfield', 299.99, 'Xbox Series X', 12),
        ('Cyberpunk 2077', 199.99, 'PC', 20),
        ('Halo Infinite', 99.99, 'Xbox Series X', 5),
        ('Final Fantasy XVI', 349.99, 'PlayStation 5', 7),
        ('Baldur\'s Gate 3', 299.99, 'PC', 10),
        ('Call of Duty: Modern Warfare III', 349.99, 'PlayStation 5', 14),
        ('Mario Kart 8 Deluxe', 279.99, 'Nintendo Switch', 18),
        ('Fortnite', 0.00, 'PC', 999),
    ]
    
    try:
        for jogo in jogos:
            cursor.execute('SELECT id FROM jogos WHERE nome = ?', (jogo[0],))
            if not cursor.fetchone():
                cursor.execute(
                    'INSERT INTO jogos (nome, preco, plataforma, quantidade) VALUES (?, ?, ?, ?)',
                    jogo
                )
        print(f'✓ {len(jogos)} jogos adicionados/verificados')
    except Exception as e:
        print(f'✗ Erro ao inserir jogos: {e}')
    
    # Inserir clientes
    clientes = [
        ('João Silva', 'joao@email.com', '11-98765-4321'),
        ('Maria Santos', 'maria@email.com', '11-99876-5432'),
        ('Pedro Oliveira', 'pedro@email.com', '11-97654-3210'),
        ('Ana Costa', 'ana@email.com', '11-96543-2109'),
        ('Carlos Ferreira', 'carlos@email.com', '11-95432-1098'),
    ]
    
    try:
        for cliente in clientes:
            cursor.execute('SELECT id FROM clientes WHERE email = ?', (cliente[1],))
            if not cursor.fetchone():
                cursor.execute(
                    'INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)',
                    cliente
                )
        print(f'✓ {len(clientes)} clientes adicionados/verificados')
    except Exception as e:
        print(f'✗ Erro ao inserir clientes: {e}')
    
    # Inserir vendas (últimos 30 dias)
    vendas_count = 0
    try:
        cursor.execute('SELECT COUNT(*) FROM vendas')
        existing_vendas = cursor.fetchone()[0]
        
        if existing_vendas == 0:
            cursor.execute('SELECT id FROM jogos')
            jogo_ids = [row[0] for row in cursor.fetchall()]
            
            cursor.execute('SELECT id FROM clientes')
            cliente_ids = [row[0] for row in cursor.fetchall()]
            
            for i in range(15):
                data = datetime.now() - timedelta(days=random.randint(0, 30))
                cursor.execute(
                    'INSERT INTO vendas (cliente_id, jogo_id, quantidade, data) VALUES (?, ?, ?, ?)',
                    (random.choice(cliente_ids), random.choice(jogo_ids), random.randint(1, 3), data.isoformat())
                )
                vendas_count += 1
            
            print(f'✓ {vendas_count} vendas adicionadas')
        else:
            print(f'✓ Banco já contém {existing_vendas} vendas')
    except Exception as e:
        print(f'✗ Erro ao inserir vendas: {e}')
    
    conn.commit()
    conn.close()
    print('\n✓ Seed finalizado com sucesso!')

if __name__ == '__main__':
    seed_database()
