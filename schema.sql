-- Schema SQL para MySQL
-- Execute este arquivo no MySQL para criar as tabelas

CREATE DATABASE IF NOT EXISTS loja_db;
USE loja_db;

CREATE TABLE IF NOT EXISTS jogos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    plataforma VARCHAR(100) NOT NULL,
    quantidade INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    telefone VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para melhor performance
CREATE INDEX idx_jogos_nome ON jogos(nome);
CREATE INDEX idx_jogos_plataforma ON jogos(plataforma);
CREATE INDEX idx_clientes_email ON clientes(email);