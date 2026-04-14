# Configuração do banco de dados MySQL
# Renomeie este arquivo para config.py e preencha com suas credenciais

DATABASE_CONFIG = {
    'host': 'localhost',          # Endereço do servidor MySQL
    'user': 'root',               # Seu usuário MySQL
    'password': 'sua_senha_aqui', # Sua senha MySQL
    'database': 'loja_db',        # Nome do banco
    'charset': 'utf8mb4',         # Charset para suporte a caracteres especiais
    'autocommit': True            # Auto-commit para transações
}

# Configurações da aplicação Flask
SECRET_KEY = 'sua_chave_secreta_aqui'  # Para sessões e segurança
DEBUG = True                           # Modo debug (False em produção)