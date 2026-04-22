import psycopg2

DB_CONFIG = {
    'dbname': 'manutencao_db',
    'user': 'postgres',
    'password': '123', 
    'host': 'localhost',
    'port': '5432'
}

def criar_tabela():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS requisicoes (
                codigo VARCHAR(10) PRIMARY KEY,
                descricao TEXT NOT NULL,
                acao_realizada TEXT,
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