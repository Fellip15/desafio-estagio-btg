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

## DDL e DML
Nesse tópico será comentado o desenvolvimento dos códigos DDL e DML.

### DDL (Data Definition Language)
São os comandos que interagem com os objetos do banco. EX: CREATE, ALTER e DROP.
Para isso foram criados os códigos que criam as tabelas utilizadas: cliente, conta, telefones e movimentacao

Nesse código foi criado as tabelas e utilizado os *constraints* para manutenção dos dados e para especificação de algumas regras, como por exemplo:
```sql
CONSTRAINT pk_telefones PRIMARY KEY (cliente_tel, telefone),
CONSTRAINT fk_telefones FOREIGN KEY (cliente_tel) REFERENCES cliente (cpf) ON DELETE CASCADE
```
que está na tabela de telefones e define a chave primária composta na primeira linha e define também que _cliente_tel_ se referencia à tabela de clientes pelo atributo cpf, além de definir que ao excluir um cliente, o telefone em que é referenciado à ele também deve ser excluido (*ON DELETE CASCADE*).

Um outro constraint pouco diferente que foi utilizado foi na tabela de movimentações, que define que o tipo deve ser apenas 's' ou 'd' (saque ou depósito):
```sql
CONSTRAINT tipo_movimentacao CHECK (LOWER(tipo) IN ('d', 's')),
```

### DML (Data Manipulation Language) 
São os comandos que interagem com os dados dentro das tabelas. EX: INSERT, DELETE e UPDATE. 
Para isso foram criados códigos que inserem, atualizam e excluem dados das tabelas. 

Para esse código não há nada a comentar mais profundamente, já que é apenas consultas, inserções e atualizações feitas para teste.

## API
### Preparando o ambiente
Primeiro é necessário instalar o postgresql, o qual foi o banco de dados relacional utilizado para o desenvolvimento do desafio:
```bash
sudo apt-get -y install postgresql
```
Após isso, é indispensável instalar o mysqlclient e o psycopg2 (biblioteca do python utilizado para acessar o banco):
```bash
pip3 install mysqlclient
pip3 install psycopg2
```
Com isso, é possível instalar a última biblioteca que foi utilizada para mapear as tabelas e rodar as query's, sqlalchemy:
```bash
pip install flask psycopg2-binary SQLAlchemy
pip install Flask-SQLAlchemy
```
Ao final desses passos, o ambiente deve estar tudo ok, assim, basta apenas iniciar o servico do postgresql:
```bash
sudo service postgresql start
```
Além disso, vale lembrar que deve ser configurado, o arquivo *api/config.py*:
```python
DATABASE = 'nome_banco_dados'
DB_USERNAME = 'nome_usuario'
DB_PASSWORD = 'senha_usuario'
DB_HOST = 'localhost'
DB_PORT = 5432
```
sendo que, localhost e porta é onde o serviço inicializado do postgresql está rodando (esse caminho é o padrão).

Prontinho! Já é possível rodar o servidor.

### Rodar o servidor
Depois de configurar o ambiente é possível rodar o servidor, assim é necessário, primeiramente, baixar esse código fonte e já possuir o python3 atualizado. Após isso, basta entrar na pasta *api* e rodar:
```bash
python3 run.py
```
O serviço rodará no localhost, porta 5000, é para lá que devem ser mandadas as requisições.

Se for necessário rodar o DDL e o DML para criar as tabelas e fazer algumas inserções, exclusões e atualizações basta rodar:
```python
python3 run_ddl_dml.py
```

# Documentação
Nesse tópico será mostrado as rotas criadas e o que é necessário para chama-las.

## Rotas telefones
### Listar telefones
**Descrição:** Esta rota permite listar todos os telefones cadastrados no sistema.

**Método HTTP:** GET

**URL:** ```/api/telefones```

**Resposta:**

* Código de status: 200 (OK)
* Corpo da resposta: Uma lista de objetos JSON representando os telefones cadastrados.

**Exemplo de resposta:**

```json
[
  {
    "cliente_tel": "12345678900",
    "telefone": "(11) 98765-4321"
  },
  {
    "cliente_tel": "98765432100",
    "telefone": "(21) 98765-4321"
  }
]
```

### Obter Telefone por CPF
**Descrição:** Esta rota permite obter os telefones associados a um cliente específico, identificado pelo seu CPF.

**Método HTTP:** GET

**URL:** ```/api/telefones/<cpf>```

**Parâmetros:**

* `<cpf>`: O CPF do cliente pelo qual se deseja obter os telefones.

**Resposta:**
* Código de status: 200 (OK) se os telefones forem encontrados, ou 404 (Não encontrado) se nenhum telefone estiver associado ao cliente informado.
* Corpo da resposta: Uma lista de objetos JSON representando os telefones do cliente.

**Exemplo de resposta (sucesso):**
```json
[
  {
    "cliente_tel": "12345678900",
    "telefone": "(11) 98765-4321"
  },
  {
    "cliente_tel": "12345678900",
    "telefone": "(11) 91234-5678"
  }
]
```

**Exemplo de resposta (falha):**
```json
{
  "message": "Telefone(s) não encontrado(s)."
}
```

### Inserir Telefone
**Descrição:** Esta rota permite inserir um novo telefone associado a um cliente.

**Método:** POST

**URL:** ```/api/telefones```

Corpo da Requisição (em formato JSON):
```json
{
  "cliente_tel": "12345678900",
  "telefone": "(11) 98765-4321"
}
```

**Resposta:** 
* Código de status: 201 (Criado) se o telefone for inserido com sucesso, 400 ou 500 se houve algum erro.
* Corpo da resposta: retorna error se houve um erro com uma mensagem ou message com uma mensagem se tudo ocorreu ok

**Exemplo de resposta (sucesso):**
```json
{
  "message": "Telefone inserido com sucesso"
}
```

**Exemplo de resposta (falha):**
```json
{
  "error": "cliente_tel e telefone são campos obrigatórios"
}
```

### Atualizar Telefone
**Descrição:** Esta rota permite atualizar o número de telefone associado a um cliente específico.

**Método HTTP:** PUT

**URL:** ```/api/telefones/<tel_antigo>```

**Parâmetros:**

* `<tel_antigo>`: O número de telefone atual que se deseja atualizar.

**Corpo da Requisição (em formato JSON):**

```json
{
  "cliente_tel": "12345678900",
  "telefone": "1191234-5678"
}
```

**Resposta:**

* Código de status: 200 (OK) se o telefone for atualizado com sucesso.
* Corpo da resposta: Uma mensagem de sucesso.

**Exemplo de resposta (sucesso):**
```json
{
  "message": "Telefone atualizado com sucesso"
}
```

**Exemplo de resposta (falha):**
```json
{
  "error": "É necessário mandar o telefone novo, o antigo (url) e o cpf do cliente"
}
```
## Rotas movimentações
A API de Movimentações é uma interface para gerenciar as movimentações financeiras associadas a contas em um sistema. Abaixo estão listadas as rotas disponíveis na API, suas descrições e exemplos de uso.

### Listar Movimentações
**Descrição:** Esta rota permite listar todas as movimentações registradas no sistema.

**Método HTTP:** GET

**URL:** ```/api/movimentacoes```

**Resposta:**

* Código de status: 200 (OK)
* Corpo da resposta: Uma lista de objetos JSON representando as movimentações registradas.

**Exemplo de resposta:**
```json
[
  {
    "data_hora": "2023-07-30 09:15:00",
    "conta_mov": 12345,
    "valor": 100.00,
    "tipo": "d"
  },
  {
    "data_hora": "2023-07-30 13:30:00",
    "conta_mov": 54321,
    "valor": 50.00,
    "tipo": "s"
  }
]
```

### Obter Movimentações de uma Conta
**Descrição:** Esta rota permite obter todas as movimentações associadas a uma conta específica.

**Método HTTP:** GET

**URL:** ```/api/movimentacoes/<conta>```

**Parâmetros:**

* `<conta>`: O número da conta pela qual se deseja obter as movimentações.

**Resposta:**
* Código de status: 200 (OK) se as movimentações forem encontradas, ou 404 (Não encontrado) se nenhuma movimentação estiver associada à conta informada.
* Corpo da resposta: Uma lista de objetos JSON representando as movimentações da conta.

**Exemplo de resposta (sucesso):**
```json
[
  {
    "data_hora": "2023-07-30 09:15:00",
    "conta_mov": 12345,
    "valor": 100.00,
    "tipo": "d"
  },
  {
    "data_hora": "2023-07-30 13:30:00",
    "conta_mov": 12345,
    "valor": 50.00,
    "tipo": "s"
  }
]
```

**Exemplo de resposta (falha):**
```json
{
  "message": "Movimentação(s) não encontrada(s)."
}
```

### Inserir Movimentação
**Descrição:** Esta rota permite criar uma nova movimentação associada a uma conta.

**Método HTTP:** POST

**URL:** ```/api/movimentacoes```

**Corpo da Requisição (em formato JSON):**
```json
{
  "data_hora": "2023-07-30 09:15:00",
  "conta_mov": 12345,
  "valor": 100.00,
  "tipo": "d"
}
```

**Resposta:**
* Código de status: 201 (Criado) se a movimentação for inserida com sucesso.
* Corpo da resposta: Uma mensagem de sucesso.

**Exemplo de resposta (sucesso):**
```json
{
  "message": "Movimentação inserida com sucesso"
}
```

**Exemplo de resposta (falha):**
```json
{
  "error": "data_hora, conta_mov, valor e tipo são campos obrigatórios"
}
```

### Atualizar Movimentação
**Descrição:** Esta rota permite atualizar o valor e/ou o tipo de uma movimentação específica.

**Método HTTP:** PUT

**URL:** ```/api/movimentacoes/<data_hora>/<conta_mov>```

**Parâmetros:**

* `<data_hora>`: A data e hora da movimentação que se deseja atualizar.
* `<conta_mov>`: O número da conta da movimentação que se deseja atualizar.

**Corpo da Requisição (em formato JSON):**
```json
{
  "valor": 120.00,
  "tipo": "s"
}
```

**Resposta:**
* Código de status: 200 (OK) se a movimentação for atualizada com sucesso.
* Corpo da resposta: Uma mensagem de sucesso.

**Exemplo de resposta (sucesso):**
```json
{
  "message": "Movimentação atualizada com sucesso"
}
```

**Exemplo de resposta (falha):**
```json
{
  "error": "É necessário mandar a data_hora, conta_mov, novo valor e novo tipo"
}
```
