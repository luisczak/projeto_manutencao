Documento de Estratégia de Testes
Eduardo Luis Franczak

Funcionalidades do sistema:
	1. Criação de requisições: O sistema fornece uma interface para o usuário preencher as requisições de manutenção.
	2. Listagem das requisições: O sistema mostra uma interface com todas as requisições cadastradas.
	3. O Frontend consome a API e renderiza os registros em uma tabela com código, data/hora, descrição e ação realizada

2. Regras de negócio por funcionalidade:
Funcionalidade 1: 
-O campo ‘descricao’ é obrigatório;
-O campo ‘acao_realizada’ é obrigatório;
-O código identificador é gerado automaticamente pelo backend via UUID v4;
-A data é registrada automaticamente;
-A hora é registrada automaticamente;
-O sistema deve retornar HTTP 201 com o código gerado após inserção bem sucedida.
-Em caso de falha, o sistema retorna HTTP 400 ou HTTP 500.

Funcionalidade 2:
-A listagem retorna todos os itens registrados;
-Os registros devem ser ordenados por ordem decrescente e por data e hora;
-O sistema deve retornar HTTP 200 com array JSON contendo os arquivos;
-Em caso de falha de conexão com o banco de dados, o sistema deve retornar HTTP 500 com mensagem de erro.

Funcionalidade 3:
-O frontend realiza uma requisição GET ao carregar a página;
-A cada cadastro novo, a tabela é atualizada automaticamente;
-Erro de comunicação com a API são mostrados na tela.

Casos de testes:
	CT-01: Cadastrar informações com dados válidos
Funcionalidade: Cadastro de requisição
Pré-condição: Banco de dados ativo e tabela requisicoes existente
Entrada: descricao: “Bomba d’água com vazamento”/ acao_realizada: “Substituição do vedante”.
Ação: POST /api/requisicoes com body JSON válido
Resultado esperado: HTTP 201 com JSON contendo mensagem “sucesso” e código com 8 caracteres maiúsculos.
Tipo: Integração

CT-02: Cadastrar com campo de obrigação vazio
Funcionalidade: Cadastro de requisição
Pré-condição: Banco de dados ativo
Entrada: descricao: “”/ acao_realizada: “Troca de peça”.
Ação: POST /api/requisicoes com descrição vazio
Resultado esperado: HTTP 400 com mensagem de erro; nenhum registro inserido no banco.
Tipo: Unitário

CT-03: Listar requisições com registros existentes
Funcionalidade: Listagem de requisições
Pré-condição: Banco de dados ativo com pelo menos dois registros cadastrados
Entrada: nenhuma
Ação: GET /api/requisicoes
Resultado esperado: HTTP 200 com array JSON contendo os registros ordenados do mais recente para o antigo
Tipo: Integração

CT-04: Listar requisições com o banco de dados vazio
Funcionalidade: Listagem de requisições
Pré-condição: Banco de dados ativo e tabelasem registro
Entrada: nenhuma
Ação: GET/api/requisicoes
Resultado esperado: HTTP 200 com array JSON vazio 
Tipo: Integração

CT-05: Verificar unicidade do código gerado
Funcionalidade: Cadastro de requisição
Pré-condição: Banco de dados ativo 
Entrada: Dois POSTs consecutivos com os mesmos dados.
Ação: POST /api/requisicoes duas vezes
Resultado esperado: Ambas retornam HTTP 201 com códigos diferentes entre si
Tipo: Integração

CT-06: Comportamento com o banco de dados indisponível
Funcionalidade: Cadastro e listagem
Pré-condição: Banco de dados e Postgres desligados
Entrada: Qualquer requisição POST ou GET
Ação: POST ou GET /api/requisicoes com banco indisponível
Resultado esperado: HTTP 500 com {“erro”: “Falha na conexão com o banco de dados.”}
Tipo: Integração

CT-07: Fluxo completo via interface
Funcionalidade:Exibição do histórico no frontend
Pré-condição: Aplicação rodando e acessível no navegador 
Entrada: Usuário preenche formulário e clica em “Salvar requisição”
Ação: Integração no navegador 
Resultado esperado: Formulário é limpo após o envio e a nova requisição aparece no topo da tabela imediatamente
Tipo: E2E

