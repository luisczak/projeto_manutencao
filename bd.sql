CREATE TABLE IF NOT EXISTS requisicoes (
    codigo VARCHAR(10) PRIMARY KEY,
    descricao TEXT NOT NULL,
    acao_realizada TEXT,
    data VARCHAR(15) NOT NULL,
    hora VARCHAR(15) NOT NULL
);