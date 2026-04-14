# Projeto Loja - Flask com SQLite e MySQL

Este projeto é uma aplicação Flask simples para gerenciar jogos e clientes de uma loja.

## Funcionalidades

- Cadastro de jogos (nome, preço, plataforma, quantidade)
- Cadastro de clientes (nome, email, telefone)
- Listagem e exclusão de registros
- Interface web com botões estilizados

## Como executar

### Opção 1: SQLite (Padrão - Mais simples)

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Execute o app:
   ```bash
   python app.py
   ```

3. Acesse: http://127.0.0.1:5000/

### Opção 2: MySQL (Banco de dados profissional)

#### Pré-requisitos:
- MySQL Server instalado e rodando
- Ou Docker para executar com containers

#### Passo 1: Configurar MySQL

**Com MySQL local:**
1. Instale MySQL Server
2. Crie o banco: `CREATE DATABASE loja_db;`
3. Execute o schema: `mysql -u root -p loja_db < schema.sql`

**Com Docker:**
```bash
docker-compose up -d mysql
```

#### Passo 2: Configurar aplicação

1. Copie `config_example.py` para `config.py`
2. Edite `config.py` com suas credenciais MySQL
3. Ou use `.env`: copie `.env.example` para `.env` e configure

#### Passo 3: Executar migração
```bash
python migrate.py
```

#### Passo 4: Executar aplicação
```bash
python app.py
```

**Com Docker (tudo junto):**
```bash
docker-compose up
```

## Estrutura do Banco

### SQLite (padrão)
- Arquivo: `LojaDB.db`
- Tabelas: `jogos` e `clientes`

### MySQL
- Servidor MySQL
- Banco: `loja_db`
- Tabelas: `jogos` e `clientes` (com timestamps)

## Arquivos do Projeto

- `app.py` - Aplicação principal Flask
- `requirements.txt` - Dependências Python
- `schema.sql` - Schema do banco MySQL
- `config_example.py` - Exemplo de configuração
- `migrate.py` - Script de migração do banco
- `.env.example` - Variáveis de ambiente
- `docker-compose.yml` - Configuração Docker
- `Dockerfile` - Container da aplicação
- `.gitignore` - Arquivos ignorados pelo Git

## Rotas

- `/` - Lista jogos
- `/cadastrar` - Cadastrar jogo
- `/clientes` - Lista clientes
- `/clientes/cadastrar` - Cadastrar cliente
- `/clientes/deletar/<id>` - Deletar cliente

## Tecnologias

- Flask
- SQLite (padrão) ou MySQL
- HTML/CSS (inline)
- Docker (opcional)