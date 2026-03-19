# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import uuid

app = Flask(__name__)

# --- CONFIGURAÇÃO DO BANCO ---
DB_CONFIG = {
    'dbname': 'manutencao_db',
    'user': 'postgres',
    'password': 'postgres', 
    'host': 'localhost',
    'port': '5432'
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/requisicoes', methods=['GET', 'POST'])
def gerenciar_requisicoes():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        if request.method == 'POST':
            dados = request.get_json()
            codigo = str(uuid.uuid4())[:8].upper()
            data_atual = datetime.now().strftime('%d/%m/%Y')
            hora_atual = datetime.now().strftime('%H:%M:%S')
            
            # Usei 'descricao' (o nome exato que está no banco)
            cursor.execute(
                'INSERT INTO requisicoes (codigo, descricao, acao_realizada, data, hora) VALUES (%s, %s, %s, %s, %s)',
                (codigo, dados['descricao'], dados['acao_realizada'], data_atual, hora_atual)
            )
            conn.commit()
            return jsonify({'mensagem': 'Sucesso!', 'codigo': codigo}), 201

        # Busca simples
        cursor.execute('SELECT * FROM requisicoes ORDER BY data DESC, hora DESC')
        requisicoes = cursor.fetchall()
        return jsonify(requisicoes)

    except Exception:
        print("Erro: Nao consegui conectar ao Banco de Dados.")
        print("DICA: Verifique se a senha no DB_CONFIG esta correta!")
        return jsonify({'erro': 'Falha na conexao'}), 500
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    print("Servidor iniciando...")
    app.run(host='0.0.0.0', port=5000, debug=True)