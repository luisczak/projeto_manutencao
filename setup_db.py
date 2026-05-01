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
                codigo VARCHAR(20) PRIMARY KEY,
                setor VARCHAR(100) NOT NULL,
                maquina VARCHAR(100) NOT NULL,
                tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('eletrico', 'mecanico')),
                categoria VARCHAR(30) NOT NULL CHECK (categoria IN ('corretiva_parada', 'melhoria')),
                motivo TEXT NOT NULL,
                mecanico VARCHAR(100) NOT NULL,
                supervisor VARCHAR(100) NOT NULL,
                status VARCHAR(20) NOT NULL DEFAULT 'aberta' CHECK (status IN ('aberta', 'realizada', 'cancelada')),
                data_abertura VARCHAR(15) NOT NULL,
                hora_abertura VARCHAR(15) NOT NULL,
                data_realizacao VARCHAR(15),
                hora_realizacao VARCHAR(15),
                observacao TEXT
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