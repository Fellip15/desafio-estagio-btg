from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from execute_query import execute_query

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fellip:fellip@localhost/db'

# Inicializar o SQLAlchemy para cada modelo
db = SQLAlchemy(app)

from models.Cliente import Cliente
from models.Conta import Conta

from routes.Cliente import cliente_bp
from routes.Conta import conta_bp

app.register_blueprint(cliente_bp)
app.register_blueprint(conta_bp)


@app.route('/api/telefones/<cpf>', methods=['GET'])
def obter_telefones(cpf):
    if cpf is None:
        return jsonify({'error': 'O cpf não pode ser nulo'})
    
    query = "SELECT telefone FROM telefones WHERE cliente_tel = %s;"

    telefones = execute_query(query, (cpf,))
    if len(telefones) <= 0:
        return jsonify([]), 200
    
    return jsonify([tel['telefone'] for tel in telefones]), 200

@app.route('/api/telefones', methods=['POST'])
def inserir_telefone():
    data = request.get_json()

    cpf = data.get("cpf")
    telefone = data.get("telefone")

    if None in [cpf, telefone]:
        return jsonify({'error': 'O cpf e o numero de telefones não podem ser nulos'})
    
    query = """
        INSERT INTO telefones (cliente_tel, telefone)
        VALUES (%s, %s);
    """

    execute_query(query, (cpf, telefone), fetchall=False)
    
    return jsonify({'message': 'Telefone adicionado com sucesso'}), 200

@app.route('/api/movimentacoes/<numero_conta>', methods=['GET'])
def buscar_movimentacoes_conta(numero_conta):
    query = "SELECT * FROM movimentacao WHERE conta_numero = %s;"

    resultado = execute_query(query, (numero_conta,))

    return jsonify(resultado), 200

@app.route('/api/movimentacoes', methods=['POST'])
def cadastrar_movimentacao():
    data = request.get_json()

    conta_numero = data.get("conta_numero")
    tipo = data.get("tipo")
    valor = data.get("valor")

    # Verificar se os campos obrigatórios foram fornecidos
    if None in [conta_numero, tipo, valor]:
        return jsonify({'error': 'O numero da conta, o tipo e o valor da movimentação são obrigatórios.'}), 400

    # Montar a consulta SQL para cadastrar a nova movimentação
    query = "INSERT INTO movimentacao (conta_numero, tipo, valor) VALUES (%s, %s, %s);"
    valores = (conta_numero, tipo, valor)

    execute_query(query, valores, fetchall=False)

    return jsonify({'message': 'Movimentação criada com sucesso'}), 200

if __name__ == '__main__':
    app.run(debug=True)