from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import os
from urllib.parse import urlparse

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')

CORS(app)

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/manutencao_db')
parsed = urlparse(DATABASE_URL)

DB_CONFIG = {
    'dbname': parsed.path.lstrip('/'),
    'user': parsed.username,
    'password': parsed.password,
    'host': parsed.hostname,
    'port': str(parsed.port or 5432)
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

            campos_obrigatorios = ['codigo', 'setor', 'maquina', 'tipo', 'categoria', 'motivo', 'mecanico', 'supervisor']
            for campo in campos_obrigatorios:
                if not dados.get(campo):
                    return jsonify({'erro': f'Campo {campo} é obrigatório'}), 400

            data_atual = datetime.now().strftime('%d/%m/%Y')
            hora_atual = datetime.now().strftime('%H:%M:%S')

            cursor.execute(
                '''INSERT INTO requisicoes 
                   (codigo, setor, maquina, tipo, categoria, motivo, mecanico, supervisor, status, data_abertura, hora_abertura, observacao)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'aberta', %s, %s, %s)''',
                (
                    dados['codigo'], dados['setor'], dados['maquina'],
                    dados['tipo'], dados['categoria'], dados['motivo'],
                    dados['mecanico'], dados['supervisor'],
                    data_atual, hora_atual, dados.get('observacao', '')
                )
            )
            conn.commit()
            return jsonify({'mensagem': 'Sucesso!', 'codigo': dados['codigo']}), 201

        # GET com filtros
        status_filtro = request.args.get('status', '')
        busca = request.args.get('busca', '')

        query = 'SELECT * FROM requisicoes WHERE 1=1'
        params = []

        if status_filtro and status_filtro != 'todos':
            query += ' AND status = %s'
            params.append(status_filtro)

        if busca:
            query += ' AND (codigo ILIKE %s OR maquina ILIKE %s OR mecanico ILIKE %s OR setor ILIKE %s)'
            params.extend([f'%{busca}%'] * 4)

        query += ' ORDER BY data_abertura DESC, hora_abertura DESC'

        cursor.execute(query, params)
        requisicoes = cursor.fetchall()
        return jsonify(requisicoes)

    except psycopg2.IntegrityError:
        return jsonify({'erro': 'Código já existe'}), 409
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({'erro': 'Falha na conexao'}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/requisicoes/<codigo>', methods=['GET', 'PUT'])
def requisicao_por_codigo(codigo):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        if request.method == 'GET':
            cursor.execute('SELECT * FROM requisicoes WHERE codigo = %s', (codigo,))
            req = cursor.fetchone()
            if not req:
                return jsonify({'erro': 'Não encontrada'}), 404
            return jsonify(req)

        if request.method == 'PUT':
            dados = request.get_json()

            cursor.execute(
                '''UPDATE requisicoes SET
                   setor = %s, maquina = %s, tipo = %s, categoria = %s,
                   motivo = %s, mecanico = %s, supervisor = %s, status = %s,
                   data_realizacao = %s, hora_realizacao = %s, observacao = %s
                   WHERE codigo = %s''',
                (
                    dados.get('setor'), dados.get('maquina'),
                    dados.get('tipo'), dados.get('categoria'),
                    dados.get('motivo'), dados.get('mecanico'),
                    dados.get('supervisor'), dados.get('status'),
                    dados.get('data_realizacao'), dados.get('hora_realizacao'),
                    dados.get('observacao'), codigo
                )
            )
            conn.commit()
            return jsonify({'mensagem': 'Atualizado com sucesso!'})

    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({'erro': 'Falha na operacao'}), 500
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    print("Servidor iniciando...")
    app.run(host='0.0.0.0', port=5000, debug=True)