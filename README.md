# Desafio estágio BTG Pactual

## Introdução

Nesse repositório será desenvolvido o desafio de estágio no processo do BTG, que consiste em modelar um banco de dados relacional com os seguintes dados das entidades:
* Dados do cliente
* Dados da conta
* Dados de movimentação (apenas depósitos e saques)

Após isso, serão entregues alguns artefatos, os quais são:
* Diagrama Entidade Relacionamento
* Modelo Entidade Relacionamento
* Scripts DDL e DML (opcional para front)
* API (opcional para front):
  * Cadastro/atualização de conta/cliente
  * Cadastro de movimentações
  * Consulta por conta/cliente
  * Consulta por movimentações de uma conta

## Modelagem do banco de dados

Após uma breve análise foi possível chegar a conclusão de quais dados devem ser armazenados para cada entidade e quais as entidades que serão criadas para esse banco de dados. As entidades serão: cliente, conta e movimentação, sendo que a movimentação é uma entidade que deriva do relacionamento entre contas, ou seja, as relações que geram os depósitos e saques.

### Dados das entidades
#### Cliente:
Para o cliente, será necessário armazenar os dados:
* CPF: string (chave primária)
* Nome completo: string
* Endereço: atributo composto
* Email: string
* Data de nascimento: string
* Telefones de contato: multivalorado

Sendo que, o cliente é uma entidade forte, ou seja, independe das outras para existir, possui sentido por si só.

#### Conta:
Já para a conta, é impensindível armazenar os seguintes dados:
* Número da conta: chave primária
* Saldo: big decimal
* Limite de movimentação: big unsigned decimal
* Senha: string

A conta também será uma entidade forte.

#### Movimentações:
É a entidade menos complexa do banco de dados:
* Valor da movimentação: big decimal
* Tipo da movimentação: string pré definida (saque, depósito)
* Data e hora da movimentação: string

Essa entidade é fraca, possuindo sentido apenas se existir contas, pois só existem movimentações se também houver contas.

## Diagramas
### MER
Para a construção do MER (Modelo Entidade Relacionamemto) foram considerados os dados falados anteriormente.
<img src="Diagramas/MER.jpg" alt="MER"/>
Dessa forma, analisando o modelo desenolvido, podemos dizer que o cliente possui CPF (chave primária), Endereço (o qual é um atributo composto, que pode ser derivado em CEP, número da casa, rua, bairro, cidade e estado), nome, email, data de nascimento e telefones para contato (atributo multivalorado, ou seja, podem ser um array com vários valores). O cliente possui uma relação de 1 para N com as contas, ou seja, um cliente possui uma ou mais contas.
Além disso, temos a entidade conta, a qual possui um número da conta (chave primária), o saldo que ela possui, o limite das movimentações que o cliente pode fazer e a senha que é necessária para conectar nela. A conta possui um relacionametno de 1 para N com a movimentação, além da movimentação ser uma entidade fraca em relação à conta, ou seja, a movimentação só existe se a conta existir e uma conta pode ter 1 ou mais movimentações.
E ainda, descrevendo a entidade movimentação: ela possui um valor que foi movimentado, o tipo da movimentação e a data hora, a qual será a chave primária (além do número da conta que é necessário utilizar já que a movimetação é ligada a uma conta).

### DER
Após a criação do MER foi criado o DER (Diagrama de entidade relacionamento), o qual mostrará mais claramente como o banco irá ser montado.
<img src="Diagramas/DER.jpg" alt="DER"/>
É possível notar que o cliente possui a chave primária CPF, e também que os valores do nome e do email desse cliente não podem ser nulos, já os outros campos são opcionais de acordo com cada serviço utilizado, como, por exemplo, se o cliente for fazer um pedido de cartão é necessário incluir o endereço. A diferença entre o cliente do MER e do DER é que no DER ele não possui o atributo telefones, pois, como ele é um atributo multivalorado foi escolhido criar uma tabela separada para que a manupulação dos telefones fique mais completa, assim, cada usuário possui um ou mais telefones. Vale notar que a tabela telefone possui uma chave composta, em que cliente é uma chave estrageira ligada ao cliente e telefone é o próprio telefone dele.
A tabela de conta possuí a chave primária e também uma chave estrangeira, ligada também à tabela cliente, pelo cpf que é a chave primária do cliente. Além de não permitir que o cliente, o saldo e a senha sejam nulos.
Por último ficou a tabela de movimentações, a qual possui uma chave composta, sendo a data e hora da movimentação e o número da conta, a qual é uma chave estrangeira para a tabela de contas.
