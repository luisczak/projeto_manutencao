Documento de Estratégia de Testes
Eduardo Luis Franczak

Funcionalidades do sistema:
	1. Criação de requisições: O sistema fornece uma interface para o usuário preencher os dados da requisição de manutenção, incluindo código, setor, máquina, tipo, categoria, motivo, mecânico responsável e supervisor.
	2. Listagem das requisições: O sistema exibe todas as requisições cadastradas em uma tabela com filtros por status e busca por texto.
	3. Edição de requisições: O sistema permite editar qualquer campo de uma requisição existente, incluindo atualização de status (Aberta, Realizada, Cancelada) e data/hora de realização.
	4. O Frontend consome a API e renderiza os registros em uma tabela com código, data/hora de abertura, setor/máquina, tipo, categoria, motivo, mecânico, status e data/hora de realização.

2. Regras de negócio por funcionalidade:

Funcionalidade 1:
- O campo 'codigo' é obrigatório e único (chave primária);
- O campo 'setor' é obrigatório;
- O campo 'maquina' é obrigatório;
- O campo 'tipo' é obrigatório e aceita apenas os valores 'eletrico' ou 'mecanico';
- O campo 'categoria' é obrigatório e aceita apenas os valores 'corretiva_parada' ou 'melhoria';
- O campo 'motivo' é obrigatório;
- O campo 'mecanico' é obrigatório;
- O campo 'supervisor' é obrigatório;
- O campo 'observacao' é opcional;
- O status é definido automaticamente como 'aberta' no momento do cadastro;
- A data e hora de abertura são registradas automaticamente pelo backend;
- O sistema deve retornar HTTP 201 com o código da requisição após inserção bem sucedida;
- Em caso de código duplicado, o sistema retorna HTTP 409;
- Em caso de falha de conexão com o banco, o sistema retorna HTTP 500.

Funcionalidade 2:
- A listagem retorna todos os registros por padrão;
- Os registros são ordenados por data e hora de abertura em ordem decrescente;
- A listagem aceita filtro por status via parâmetro de query (?status=aberta, ?status=realizada, ?status=cancelada);
- A listagem aceita busca por texto via parâmetro de query (?busca=), pesquisando em código, máquina, mecânico e setor;
- O sistema deve retornar HTTP 200 com array JSON contendo os registros;
- Em caso de falha de conexão com o banco, o sistema retorna HTTP 500.

Funcionalidade 3:
- O sistema permite editar todos os campos de uma requisição existente;
- O status pode ser alterado para 'aberta', 'realizada' ou 'cancelada';
- Os campos data_realizacao e hora_realizacao são preenchidos manualmente ou via botão "Usar data/hora atual";
- O sistema deve retornar HTTP 200 com mensagem de sucesso após atualização;
- Em caso de falha, o sistema retorna HTTP 500.

Funcionalidade 4:
- O frontend realiza uma requisição GET ao carregar a página;
- Os cards de estatísticas (Total, Em Aberto, Realizadas, Canceladas) são atualizados automaticamente a cada operação;
- A tabela é atualizada automaticamente após cada cadastro ou edição;
- O formulário é limpo após o envio com sucesso.

Casos de testes:

CT-01: Cadastrar requisição com dados válidos
Funcionalidade: Cadastro de requisição
Pré-condição: Banco de dados ativo e tabela requisicoes existente
Entrada: codigo: "22805", setor: "Laminação", maquina: "Torno Roleteiro", tipo: "mecanico", categoria: "corretiva_parada", motivo: "Vazamento no vedante", mecanico: "João Silva", supervisor: "Carlos Souza"
Ação: POST /api/requisicoes com body JSON válido
Resultado esperado: HTTP 201 com JSON contendo mensagem "Sucesso!" e o código informado. Status registrado automaticamente como "aberta".
Tipo: Integração

CT-02: Cadastrar com campo obrigatório vazio
Funcionalidade: Cadastro de requisição
Pré-condição: Banco de dados ativo
Entrada: codigo: "22806", setor: "", demais campos preenchidos.
Ação: POST /api/requisicoes com campo setor vazio
Resultado esperado: HTTP 400 com mensagem de erro indicando o campo obrigatório ausente; nenhum registro inserido no banco.
Tipo: Unitário

CT-03: Cadastrar com código duplicado
Funcionalidade: Cadastro de requisição
Pré-condição: Banco de dados ativo com requisição de código "22805" já cadastrada
Entrada: Mesmo código "22805" com dados diferentes
Ação: POST /api/requisicoes com código já existente
Resultado esperado: HTTP 409 com mensagem "Código já existe"; nenhum novo registro inserido.
Tipo: Integração

CT-04: Listar requisições com registros existentes
Funcionalidade: Listagem de requisições
Pré-condição: Banco de dados ativo com pelo menos dois registros cadastrados
Entrada: nenhuma
Ação: GET /api/requisicoes
Resultado esperado: HTTP 200 com array JSON contendo os registros ordenados do mais recente para o mais antigo
Tipo: Integração

CT-05: Listar requisições filtrando por status
Funcionalidade: Listagem com filtro
Pré-condição: Banco de dados ativo com registros de status variados
Entrada: status=aberta
Ação: GET /api/requisicoes?status=aberta
Resultado esperado: HTTP 200 com array JSON contendo apenas os registros com status "aberta"
Tipo: Integração

CT-06: Listar requisições com busca por texto
Funcionalidade: Listagem com busca
Pré-condição: Banco de dados ativo com registros cadastrados
Entrada: busca=Torno
Ação: GET /api/requisicoes?busca=Torno
Resultado esperado: HTTP 200 com array JSON contendo apenas os registros que contenham "Torno" em código, máquina, mecânico ou setor
Tipo: Integração

CT-07: Listar requisições com banco de dados vazio
Funcionalidade: Listagem de requisições
Pré-condição: Banco de dados ativo e tabela sem registros
Entrada: nenhuma
Ação: GET /api/requisicoes
Resultado esperado: HTTP 200 com array JSON vazio
Tipo: Integração

CT-08: Editar uma requisição existente
Funcionalidade: Edição de requisição
Pré-condição: Banco de dados ativo com requisição de código "22805" cadastrada
Entrada: status: "realizada", data_realizacao: "02/05/2026", hora_realizacao: "14:30:00"
Ação: PUT /api/requisicoes/22805 com body JSON contendo os campos atualizados
Resultado esperado: HTTP 200 com mensagem "Atualizado com sucesso!"; registro atualizado no banco com os novos dados.
Tipo: Integração

CT-09: Editar requisição inexistente
Funcionalidade: Edição de requisição
Pré-condição: Banco de dados ativo
Entrada: codigo: "99999" (não existe)
Ação: PUT /api/requisicoes/99999
Resultado esperado: HTTP 500 com mensagem de falha na operação
Tipo: Integração

CT-10: Comportamento com banco de dados indisponível
Funcionalidade: Cadastro e listagem
Pré-condição: Banco de dados e Postgres desligados
Entrada: Qualquer requisição POST, GET ou PUT
Ação: POST ou GET /api/requisicoes com banco indisponível
Resultado esperado: HTTP 500 com {"erro": "Falha na conexao"}
Tipo: Integração

CT-11: Fluxo completo via interface — cadastro
Funcionalidade: Exibição do histórico no frontend
Pré-condição: Aplicação rodando e acessível no navegador
Entrada: Usuário preenche todos os campos obrigatórios e clica em "Registrar Requisição"
Ação: Interação no navegador
Resultado esperado: Formulário é limpo após o envio; a nova requisição aparece no topo da tabela; os cards de estatísticas são atualizados.
Tipo: E2E

CT-12: Fluxo completo via interface — edição e conclusão
Funcionalidade: Edição de requisição via interface
Pré-condição: Aplicação rodando com ao menos uma requisição com status "aberta"
Entrada: Usuário clica em "Editar", altera o status para "realizada", clica em "Usar data/hora atual" e salva
Ação: Interação no navegador com o modal de edição
Resultado esperado: Modal fechado após o salvamento; status da requisição atualizado para "realizada" na tabela; card "Realizadas" incrementado.
Tipo: E2E