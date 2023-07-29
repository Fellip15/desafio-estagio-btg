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
* Senha: string codificada

A conta também será uma entidade forte.

#### Movimentações:
É a entidade menos complexa do banco de dados:
* Valor da movimentação: big decimal
* Tipo da movimentação: string pré definida (saque, depósito)
* Data e hora da movimentação: string

## Diagramas
### MER
<img src="Diagramas/MER.jpg" alt="MER"/>

### DER
<img src="Diagramas/DER.jpg" alt="DER"/>
