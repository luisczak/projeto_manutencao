from flask import Flask, request, jsonify, render_template
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import uuid
import os

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')

DB_CONFIG = {
    'dbname': os.getenv('DB_NAME', 'manutencao_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432')
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)


def gerar_codigo_unico(cursor):
    """Gera um código UUID de 8 chars garantindo unicidade no banco."""
    for _ in range(10):  # tenta até 10 vezes antes de desistir
        codigo = str(uuid.uuid4())[:8].upper()
        cursor.execute('SELECT 1 FROM requisicoes WHERE codigo = %s', (codigo,))
        if cursor.fetchone() is None:
            return codigo
    raise RuntimeError("Não foi possível gerar um código único após 10 tentativas.")


def validar_campos(dados):
    """
    Valida os campos obrigatórios do body.
    Retorna (True, None) se válido, ou (False, mensagem) se inválido.
    """
    if not dados:
        return False, "Body JSON ausente ou malformado."

    descricao = dados.get('descricao', '')
    acao = dados.get('acao_realizada', '')

    if not descricao or not descricao.strip():
        return False, "O campo 'descricao' é obrigatório e não pode ser vazio."

    if not acao or not acao.strip():
        return False, "O campo 'acao_realizada' é obrigatório e não pode ser vazio."

    return True, None


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
            dados = request.get_json(silent=True)

            #Validação dos campos obrigatórios
            valido, erro = validar_campos(dados)
            if not valido:
                return jsonify({'erro': erro}), 400

            codigo = gerar_codigo_unico(cursor)
            data_atual = datetime.now().strftime('%d/%m/%Y')
            hora_atual = datetime.now().strftime('%H:%M:%S')

            cursor.execute(
                'INSERT INTO requisicoes (codigo, descricao, acao_realizada, data, hora) '
                'VALUES (%s, %s, %s, %s, %s)',
                (codigo,
                 dados['descricao'].strip(),
                 dados['acao_realizada'].strip(),
                 data_atual,
                 hora_atual)
            )
            conn.commit()
            return jsonify({'mensagem': 'Sucesso!', 'codigo': codigo}), 201

        # GET
        cursor.execute('SELECT * FROM requisicoes ORDER BY data DESC, hora DESC')
        requisicoes = cursor.fetchall()
        return jsonify(requisicoes)

    except psycopg2.Error as e:
        print(f"Erro de banco de dados: {e}")
        return jsonify({'erro': 'Falha na conexao com o banco de dados.'}), 500

    except RuntimeError as e:
        print(f"Erro interno: {e}")
        return jsonify({'erro': str(e)}), 500

    except Exception as e:
        print(f"Erro inesperado: {e}")
        return jsonify({'erro': 'Erro interno no servidor.'}), 500

    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    debug = os.getenv('DEBUG', 'true').lower() == 'true'
    print("Servidor iniciando...")
    app.run(host='0.0.0.0', port=5000, debug=debug)