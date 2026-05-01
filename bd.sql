CREATE TABLE IF NOT EXISTS requisicoes (
    codigo VARCHAR(20) PRIMARY KEY,
    setor VARCHAR(100) NOT NULL,
    maquina VARCHAR(100) NOT NULL,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('eletrico', 'mecanico')),
    categoria VARCHAR(30) NOT NULL CHECK (categoria IN ('corretiva_parada', 'melhoria')),
    motivo TEXT NOT NULL,
    mecanico VARCHAR(100) NOT NULL,
    supervisor VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'aberta' CHECK (status IN ('aberta', 'realizada', 'cancelada')),
    data_abertura VARCHAR(15) NOT NULL,
    hora_abertura VARCHAR(15) NOT NULL,
    data_realizacao VARCHAR(15),
    hora_realizacao VARCHAR(15),
    observacao TEXT
);