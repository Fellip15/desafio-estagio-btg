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
* id: identificador
* Nome completo: string
* Endereço: string ou entidade completa separada (fraca)
* Email: string
* CPF: string
* Foto: imagem
* Data de nascimento: string
* Número da conta: identificador da entidade conta

Sendo que, o cliente é uma entidade forte, ou seja, independe das outras para existir, possui sentido por si só.

#### Conta:
Já para a conta, é impensindível armazenar os seguintes dados:
* id: identificador
* Número da conta: string ou inteiro grande
* Valor total: big decimal
* Limite de transação: big unsigned decimal (talvez criar uma entidade separada que guarda o tipo da movimentação e o limite dela pra essa conta)
* Limite de crédito: big unsigned decimal (se for feito o parentesis acima, exclui isso)
* Senha: string codificada

A conta também será uma entidade forte.

#### Movimentações:
É a entidade menos complexa do banco de dados:
* id: identificador
* Valor da movimentação: big decimal
* Tipo da movimentação: string pré definida (saque, depósito, etc)
* Data da movimentação: string
* Id conta source: identificador da entidade conta
* Id conta destino: identificador da entidade conta

Entidade associativa, pois ela apenas representará o relacionamento entre as contas, ou seja, representará as transações. Para o tipo movimentação saque e depósito não será necessário o id da conta destino, já que será uma movimentação unilateral.
