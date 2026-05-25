import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from unittest.mock import patch, MagicMock
from app import app


@pytest.fixture
def client():
    """Fixture: cliente de teste Flask com TESTING=True"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def make_mock_conn():
    """Helper: retorna uma conexão mockada pronta para uso."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn, mock_cursor


PAYLOAD_VALIDO = {
    'codigo': 'REQ-001',
    'setor': 'Produção',
    'maquina': 'Torno CNC',
    'tipo': 'Corretiva',
    'categoria': 'Mecânica',
    'motivo': 'Eixo quebrado',
    'mecanico': 'João Silva',
    'supervisor': 'Carlos Souza',
    'observacao': 'Urgente'
}
# CT-02 — Cadastrar com campo obrigatório vazio
# Tipo: Unitário

def test_ct02_campo_codigo_vazio_retorna_400(client):
    """CT-02: POST sem 'codigo' deve retornar HTTP 400 antes de tocar no banco."""

    # ARRANGE
    mock_conn, _ = make_mock_conn()
    payload = {**PAYLOAD_VALIDO, 'codigo': ''}

    # ACT
    with patch('app.get_db_connection', return_value=mock_conn):
        resposta = client.post('/api/requisicoes', json=payload)

    # ASSERT
    assert resposta.status_code == 400
    assert 'erro' in resposta.get_json()


def test_ct02_campo_setor_vazio_retorna_400(client):
    """CT-02: POST sem 'setor' deve retornar HTTP 400."""

    # ARRANGE
    mock_conn, _ = make_mock_conn()
    payload = {**PAYLOAD_VALIDO, 'setor': ''}

    # ACT
    with patch('app.get_db_connection', return_value=mock_conn):
        resposta = client.post('/api/requisicoes', json=payload)

    # ASSERT
    assert resposta.status_code == 400
    assert 'erro' in resposta.get_json()


def test_ct02_campo_maquina_vazio_retorna_400(client):
    """CT-02: POST sem 'maquina' deve retornar HTTP 400."""

    # ARRANGE
    mock_conn, _ = make_mock_conn()
    payload = {**PAYLOAD_VALIDO, 'maquina': ''}

    # ACT
    with patch('app.get_db_connection', return_value=mock_conn):
        resposta = client.post('/api/requisicoes', json=payload)

    # ASSERT
    assert resposta.status_code == 400
    assert 'erro' in resposta.get_json()


def test_ct02_campo_mecanico_vazio_retorna_400(client):
    """CT-02: POST sem 'mecanico' deve retornar HTTP 400."""

    # ARRANGE
    mock_conn, _ = make_mock_conn()
    payload = {**PAYLOAD_VALIDO, 'mecanico': ''}

    # ACT
    with patch('app.get_db_connection', return_value=mock_conn):
        resposta = client.post('/api/requisicoes', json=payload)

    # ASSERT
    assert resposta.status_code == 400
    assert 'erro' in resposta.get_json()


def test_ct02_mensagem_erro_indica_campo_faltante(client):
    """CT-02: a mensagem de erro deve identificar qual campo está vazio."""

    # ARRANGE
    mock_conn, _ = make_mock_conn()
    payload = {**PAYLOAD_VALIDO, 'supervisor': ''}

    # ACT
    with patch('app.get_db_connection', return_value=mock_conn):
        resposta = client.post('/api/requisicoes', json=payload)

    # ASSERT
    dados = resposta.get_json()
    assert resposta.status_code == 400
    assert 'supervisor' in dados['erro']


def test_ct02_commit_nao_chamado_quando_campo_vazio(client):
    """CT-02: nenhum dado deve ser persistido quando validação falha."""

    # ARRANGE
    mock_conn, _ = make_mock_conn()
    payload = {**PAYLOAD_VALIDO, 'motivo': ''}

    # ACT
    with patch('app.get_db_connection', return_value=mock_conn):
        client.post('/api/requisicoes', json=payload)

    # ASSERT — commit jamais deve ter sido chamado
    mock_conn.commit.assert_not_called()


# Testes adicionais para aumentar cobertura (rotas GET e PUT)

def test_get_lista_requisicoes_retorna_200(client):
    """GET /api/requisicoes deve retornar HTTP 200 com lista."""

    # ARRANGE
    mock_conn, mock_cursor = make_mock_conn()
    mock_cursor.fetchall.return_value = []

    # ACT
    with patch('app.get_db_connection', return_value=mock_conn):
        resposta = client.get('/api/requisicoes')

    # ASSERT
    assert resposta.status_code == 200
    assert isinstance(resposta.get_json(), list)


def test_get_com_filtro_status(client):
    """GET /api/requisicoes?status=aberta deve aplicar filtro corretamente."""

    # ARRANGE
    mock_conn, mock_cursor = make_mock_conn()
    mock_cursor.fetchall.return_value = []

    # ACT
    with patch('app.get_db_connection', return_value=mock_conn):
        resposta = client.get('/api/requisicoes?status=aberta')

    # ASSERT
    assert resposta.status_code == 200


def test_get_com_filtro_busca(client):
    """GET /api/requisicoes?busca=torno deve aplicar busca por texto."""

    # ARRANGE
    mock_conn, mock_cursor = make_mock_conn()
    mock_cursor.fetchall.return_value = []

    # ACT
    with patch('app.get_db_connection', return_value=mock_conn):
        resposta = client.get('/api/requisicoes?busca=torno')

    # ASSERT
    assert resposta.status_code == 200


def test_get_requisicao_por_codigo_encontrada(client):
    """GET /api/requisicoes/<codigo> deve retornar a requisição quando existe."""

    # ARRANGE
    mock_conn, mock_cursor = make_mock_conn()
    mock_cursor.fetchone.return_value = {'codigo': 'REQ-001', 'setor': 'Produção'}

    # ACT
    with patch('app.get_db_connection', return_value=mock_conn):
        resposta = client.get('/api/requisicoes/REQ-001')

    # ASSERT
    assert resposta.status_code == 200
    assert resposta.get_json()['codigo'] == 'REQ-001'


def test_get_requisicao_por_codigo_nao_encontrada(client):
    """GET /api/requisicoes/<codigo> deve retornar 404 quando não existe."""

    # ARRANGE
    mock_conn, mock_cursor = make_mock_conn()
    mock_cursor.fetchone.return_value = None

    # ACT
    with patch('app.get_db_connection', return_value=mock_conn):
        resposta = client.get('/api/requisicoes/INEXISTENTE')

    # ASSERT
    assert resposta.status_code == 404
    assert 'erro' in resposta.get_json()


def test_put_atualiza_requisicao_com_sucesso(client):
    """PUT /api/requisicoes/<codigo> deve atualizar e retornar mensagem de sucesso."""

    # ARRANGE
    mock_conn, mock_cursor = make_mock_conn()
    payload = {**PAYLOAD_VALIDO, 'status': 'concluida',
               'data_realizacao': '25/05/2026', 'hora_realizacao': '14:00:00'}

    # ACT
    with patch('app.get_db_connection', return_value=mock_conn):
        resposta = client.put('/api/requisicoes/REQ-001', json=payload)

    # ASSERT
    assert resposta.status_code == 200
    assert 'mensagem' in resposta.get_json()


def test_post_codigo_duplicado_retorna_409(client):
    """POST com código já existente deve retornar HTTP 409."""

    # ARRANGE
    mock_conn, mock_cursor = make_mock_conn()
    import psycopg2
    mock_cursor.execute.side_effect = psycopg2.IntegrityError("duplicate key")

    # ACT
    with patch('app.get_db_connection', return_value=mock_conn):
        resposta = client.post('/api/requisicoes', json=PAYLOAD_VALIDO)

    # ASSERT
    assert resposta.status_code == 409
    assert 'erro' in resposta.get_json()


def test_post_falha_banco_retorna_500(client):
    """POST com banco indisponível deve retornar HTTP 500."""

    # ARRANGE — simula falha na conexão
    # ACT
    with patch('app.get_db_connection', side_effect=Exception("connection refused")):
        resposta = client.post('/api/requisicoes', json=PAYLOAD_VALIDO)

    # ASSERT
    assert resposta.status_code == 500
    assert 'erro' in resposta.get_json()