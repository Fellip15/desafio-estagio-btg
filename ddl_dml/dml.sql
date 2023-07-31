/*Adiciona um novo cliente*/
INSERT INTO cliente ( cpf, nome, email, data_nasc, 
    cep, numero_casa, rua, bairro, cidade, estado)
VALUES ( '123.456.789-00', 'João da Silva', 'joao@email.com', '1990-05-15', 
    '12345-678', 123, 'Rua das Flores', 'Centro', 'Cidade A', 'SP'
);

/*Adiciona um telefone*/
INSERT INTO telefones (cliente_tel, telefone)
VALUES ('123.456.789-00', '34999999999');

/*Adiciona uma conta*/
INSERT INTO conta (numero, cliente_conta, saldo, limite_mov, senha)
VALUES (123456789, '123.456.789-00', 1500.00, 500.00, 'minha_senha_secreta');

/*Cria uma movimentação*/
INSERT INTO movimentacao (valor, tipo, data_hora, conta_mov)
VALUES (200.00, 'd', '2023-07-29T14:30:00', 123456789);

/*Atualiza o saldo na conta*/
UPDATE conta
SET saldo = saldo - 50.00
WHERE numero = 123456789;

/*Seleciona todos os clientes e seus telefones*/
SELECT c.cpf, c.nome, t.telefone
FROM cliente c
LEFT JOIN telefones t ON c.cpf = t.cliente_tel;

/*Seleciona o valor e a data das movimentações da conta do tipo saque*/
SELECT valor, data_hora
FROM movimentacao
WHERE tipo = 's' AND conta_mov = 123456789;

/*Atualizar o e-mail de um cliente*/
UPDATE cliente
SET email = 'novo_email@email.com'
WHERE cpf = '123.456.789-00';

/*Inserir um novo telefone para um novo cliente*/
INSERT INTO cliente (
    cpf, nome, email, 
    data_nasc, cep, numero_casa, 
    rua, bairro, cidade, estado
    )
VALUES (
   '987.654.321-00', 'José Maria', 'jose@email.com', 
    '1995-05-31', '78910-678', 321, 
    'Rua das Aguas', 'Jardim Imperial', 'Cidade B', 'MG'
    );
INSERT INTO telefones (cliente_tel, telefone)
VALUES ('987.654.321-00', '888888888');

/*Atualizar o limite de movimentação*/
UPDATE conta
SET limite_mov = 1000.00
WHERE numero = 123456789;

/*Realizar uma movimentação do tipo saque*/
INSERT INTO movimentacao (valor, tipo, data_hora, conta_mov)
VALUES (100.00, 's', '2023-07-29T15:45:00', 123456789);

/*Seleciona todos os clientes que possuem contas com saldo acima de 1000.00:*/
SELECT c.nome, c.cpf
FROM cliente c
INNER JOIN conta co ON c.cpf = co.cliente_conta
WHERE co.saldo > 1000.00;

/*Seleciona todas as movimentações realizadas em uma data e em uma conta*/
SELECT valor, tipo, data_hora
FROM movimentacao
WHERE data_hora >= '2023-07-29T00:00:00' AND data_hora < '2023-07-30T00:00:00'
AND conta_mov = 123456789;

/*Excluir um cliente e todas as suas informações*/
DELETE FROM telefones
WHERE cliente_tel = '987.654.321-00';

DELETE FROM cliente
WHERE cpf = '987.654.321-00';