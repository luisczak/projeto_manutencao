import psycopg2
import os

DB_CONFIG = {
    'dbname': os.getenv('DB_NAME', 'manutencao_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432')
}

def criar_tabela():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS requisicoes (
                codigo VARCHAR(10) PRIMARY KEY,
                descricao TEXT NOT NULL CHECK (descricao <> ''),
                acao_realizada TEXT NOT NULL CHECK (acao_realizada <> ''),
                data VARCHAR(15) NOT NULL,
                hora VARCHAR(15) NOT NULL
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
        print("Sucesso: Tabela verificada/criada!")
    except Exception as e:
        print(f"Erro de conexao: {e}")

if __name__ == '__main__':
    criar_tabela()