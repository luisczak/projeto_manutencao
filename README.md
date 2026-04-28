# Sistema de Requisições de Manutenção

Este projeto é uma aplicação Full Stack simples desenvolvida para fins acadêmicos, com foco na implantação e configuração de instâncias em nuvem (AWS EC2).

## Tecnologias Utilizadas
* **Backend:** Python com framework Flask (API REST)
* **Frontend:** HTML5, CSS3 e JavaScript (Fetch API)
* **Banco de Dados:** PostgreSQL
* **Infraestrutura:** Preparado para instâncias Linux (AWS/Ubuntu)

## Funcionalidades
- Cadastro de requisições de manutenção.
- Geração automática de código identificador (UUID).
- Registro automático de data e hora local.
- Histórico de atividades integrado ao banco de dados.

## Como rodar o projeto

### 1. Configurar o Banco de Dados

Criar um banco chamado `manutencao_db`:

```sql
CREATE TABLE requisicoes (
    codigo VARCHAR(10) PRIMARY KEY,
    descricao TEXT NOT NULL CHECK (descricao <> ''),
    acao_realizada TEXT NOT NULL CHECK (acao_realizada <> ''),
    data VARCHAR(15) NOT NULL,
    hora VARCHAR(15) NOT NULL
);
```

Ou executar o script de setup:

```bash
python setup_db.py
```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. Executar a Aplicação

```bash
python src/app.py
```

Acesse em: `http://localhost:5000`

## Testes

Estratégia de testes completa: [docs/testes/estrategia_testes.md](docs/testes/estrategia_testes.md)

## Estrutura do Projeto

```
projeto/
├── src/
│   ├── app.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       └── style.css
├── docs/
│   └── testes/
│       └── estrategia_testes.md
├── setup_db.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yaml
└── README.md
```

## Variáveis de Ambiente

Para customizar a conexão com o banco de dados, use variáveis de ambiente:

```bash
DB_NAME=manutencao_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DEBUG=true
```

## Autor

Desenvolvido como projeto acadêmico de Engenharia de Software.