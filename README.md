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
1. **Configurar o Banco de Dados:**
   - Criar um banco chamado `manutencao_db`.
   - Executar o script SQL contido no arquivo de configuração ou via Query Tool:
   ```sql
   CREATE TABLE requisicoes (
       codigo VARCHAR(10) PRIMARY KEY,
       descricao TEXT NOT NULL,
       acao_realizada TEXT,
       data VARCHAR(15) NOT NULL,
       hora VARCHAR(15) NOT NULL
   );
Instalar Dependências:

Bash
pip install -r requirements.txt
Executar a Aplicação:

Bash
python app.py
Acesse em: http://localhost:5000