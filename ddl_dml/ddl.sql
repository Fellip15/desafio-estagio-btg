/*Cria a tabela clientes com a chave primária sendo o cpf*/
CREATE TABLE cliente (
    cpf CHAR(14),
    nome VARCHAR(64) NOT NULL,
    email VARCHAR(64) NOT NULL,
    data_nasc DATE,
    cep CHAR(9),
    numero_casa INT,
    rua VARCHAR(64),
    bairro VARCHAR(64),
    cidade VARCHAR(64),
    estado VARCHAR(2),

    CONSTRAINT pk_cliente PRIMARY KEY (cpf)
);

/*Cria a tabela de telefones com duas chaves primarias e uma chave estrangeira para a tabela cliente*/
CREATE TABLE telefones (
    cliente_tel CHAR(14),
    telefone CHAR(11),

    CONSTRAINT pk_telefones PRIMARY KEY (cliente_tel, telefone),
    CONSTRAINT fk_telefones FOREIGN KEY (cliente_tel) REFERENCES cliente (cpf) ON DELETE CASCADE
);

/*Cria a tabela de conta com a chave primária numero e a chave estrangeira para a tabela de cliente*/
CREATE TABLE conta (
    numero BIGINT,
    cliente_conta CHAR(14) NOT NULL,
    saldo FLOAT NOT NULL,
    limite_mov FLOAT,
    senha VARCHAR(32) NOT NULL,

    CONSTRAINT pk_conta PRIMARY KEY (numero),
    CONSTRAINT fk_conta FOREIGN KEY (cliente_conta) REFERENCES cliente (cpf) ON DELETE CASCADE
);

/*Cria a tabela de movimentação com a chave primaria composta, data_hora e o numero da conta,
com a chave estrangeira para a tabela conta e com o tipo de movimentação podendo ser apenas
's' ou 'd' (saque ou depósito)*/
CREATE TABLE movimentacao (
    valor FLOAT NOT NULL,
    tipo CHAR(1) NOT NULL,
    data_hora TIMESTAMP,
    conta_mov BIGINT,

    CONSTRAINT pk_movimentacao PRIMARY KEY (data_hora, conta_mov),
    CONSTRAINT tipo_movimentacao CHECK (LOWER(tipo) IN ('d', 's')),
    CONSTRAINT fk_movimentacao FOREIGN KEY (conta_mov) REFERENCES conta (numero) ON DELETE CASCADE
);