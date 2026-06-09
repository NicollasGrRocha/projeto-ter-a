# Loja de Jogos - Sistema de Gerenciamento

Uma aplicação web Flask para gerenciar vendas, estoque e clientes de uma loja de jogos. 

## Funcionalidades

### Para Usuários
- ✅ Visualizar catálogo de jogos disponíveis
- ✅ Ver preço, plataforma e quantidade em estoque
- ✅ Registrar compras de jogos

### Para Administradores  
- ✅ Cadastro e gerenciamento de jogos
- ✅ Cadastro e gerenciamento de clientes
- ✅ Controle de estoque em tempo real
- ✅ Registro de vendas
- ✅ Histórico completo de vendas
- ✅ **Relatório mensal** com:
  - Total de unidades vendidas no mês
  - Quantidade de transações
  - Total em estoque
  - Jogos mais vendidos
- ✅ Alertas de estoque baixo

### Banco de Dados
- Tabela `jogos`: id, nome, preço, plataforma, quantidade
- Tabela `clientes`: id, nome, email, telefone
- Tabela `vendas`: id, cliente_id, jogo_id, quantidade, data

## Instalação e Execução

### Pré-requisitos
- Python 3.8+
- pip

### Passo 1: Clonar e instalar dependências

```bash
git clone <seu-repositorio>
cd trabalho\ agil
pip install -r requirements.txt
```

### Passo 2: Inicializar banco de dados e popular com dados de exemplo

```bash
python seed.py
```

Isso criará o banco SQLite e adicionará:
- 10 jogos de exemplo
- 5 clientes de teste
- 9 vendas de exemplo dos últimos 30 dias

### Passo 3: Executar a aplicação

```bash
python app.py
```

A aplicação estará disponível em: **http://127.0.0.1:5000**

## Navegação e Rotas

### Para Usuários
- **Home**: `http://127.0.0.1:5000/user` - Ver catálogo de jogos
- **Comprar**: `http://127.0.0.1:5000/vendas/registrar` - Registrar compra

### Para Administradores
- **Admin**: `http://127.0.0.1:5000/admin` - Painel de administração
- **Cadastrar Jogo**: `http://127.0.0.1:5000/cadastrar` - Adicionar novo jogo
- **Clientes**: `http://127.0.0.1:5000/clientes` - Gerenciar clientes
- **Vendas**: `http://127.0.0.1:5000/vendas` - Ver histórico de vendas
- **Estoque**: `http://127.0.0.1:5000/estoque` - Controlar estoque
- **Relatório**: `http://127.0.0.1:5000/relatorio` - 📊 Relatório do mês atual

## Estrutura do Projeto

```
.
├── app.py                 # Aplicação Flask principal
├── seed.py               # Script para popular o banco com dados
├── LojaDB.db            # Banco de dados SQLite
├── requirements.txt      # Dependências Python
├── schema.sql           # Schema do banco de dados
├── migrate.py           # Script de migração
├── docker-compose.yml   # Composição Docker
├── Dockerfile           # Configuração Docker
├── .gitignore          # Arquivos ignorados pelo Git
└── README.md           # Este arquivo
```

## Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Banco de Dados**: SQLite (desenvolvimento), MySQL (produção opcional)
- **Frontend**: HTML5 + CSS3 + Jinja2
- **Containerização**: Docker

## Temas e Estilo

A interface usa um tema moderno com gradientes azuis escuros, botões interativos e design responsivo:
- Cores principais: Azul #2563eb (botões) e cinza #475569 (secundário)
- Design adaptável para desktop e dispositivos móveis
- Cards e seções organizadas em grid

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