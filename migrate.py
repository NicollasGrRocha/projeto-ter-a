#!/usr/bin/env python3
"""
Script de migração para inicializar o banco MySQL
Execute: python migrate.py
"""

import pymysql
from config import DATABASE_CONFIG

def create_tables():
    """Cria as tabelas no banco MySQL"""
    try:
        conn = pymysql.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()

        # Criar tabela jogos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jogos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                preco DECIMAL(10,2) NOT NULL,
                plataforma VARCHAR(100) NOT NULL,
                quantidade INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Criar tabela clientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                telefone VARCHAR(20) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Criar índices
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_jogos_nome ON jogos(nome)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_jogos_plataforma ON jogos(plataforma)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_clientes_email ON clientes(email)')

        conn.commit()
        print("✅ Tabelas criadas com sucesso!")

    except pymysql.Error as e:
        print(f"❌ Erro ao criar tabelas: {e}")
    finally:
        if conn:
            conn.close()

def insert_sample_data():
    """Insere dados de exemplo"""
    try:
        conn = pymysql.connect(**DATABASE_CONFIG)
        cursor = conn.cursor()

        # Inserir jogos de exemplo
        jogos = [
            ('The Legend of Zelda', 299.99, 'Nintendo Switch', 10),
            ('God of War', 199.99, 'PlayStation', 5),
            ('Minecraft', 89.99, 'Multiplataforma', 20)
        ]

        cursor.executemany('''
            INSERT IGNORE INTO jogos (nome, preco, plataforma, quantidade)
            VALUES (%s, %s, %s, %s)
        ''', jogos)

        # Inserir clientes de exemplo
        clientes = [
            ('João Silva', 'joao@email.com', '11999999999'),
            ('Maria Santos', 'maria@email.com', '11888888888')
        ]

        cursor.executemany('''
            INSERT IGNORE INTO clientes (nome, email, telefone)
            VALUES (%s, %s, %s)
        ''', clientes)

        conn.commit()
        print("✅ Dados de exemplo inseridos!")

    except pymysql.Error as e:
        print(f"❌ Erro ao inserir dados: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    print("🚀 Iniciando migração do banco MySQL...")
    create_tables()
    insert_sample_data()
    print("✅ Migração concluída!")