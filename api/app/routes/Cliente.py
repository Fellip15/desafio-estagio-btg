from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from sqlalchemy import or_

from app import db

from app.models.Cliente import Cliente

cliente_bp = Blueprint('cliente', __name__)

"""
    Retorna todos os clientes do banco de dados
"""
@cliente_bp.route('/api/clientes', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()

    return jsonify([c.as_dict() for c in clientes])

"""
    Retorna um ou mais clientes
    Parametro de url: parametro (nome, email ou cpf)
    no caso da busca por nome o retorno pode ser mais de um cliente
"""
@cliente_bp.route('/api/clientes/<parametro>', methods=['GET'])
def obter_cliente_parametro_url(parametro):
    clientes = Cliente.query.filter(or_(Cliente.cpf.like(parametro), Cliente.nome.contains(parametro), Cliente.email.like(parametro))).all()

    if len(clientes) <= 0:
        return jsonify({'error': "Cliente(s) não encontrado."})
    
    return jsonify([cliente.as_dict() for cliente in clientes]), 200

"""
    Cria um cliente e salva no banco de dados
    Campos obrigatorios do body: cpf, nome e email
    Demais campos são opcionais
"""
@cliente_bp.route('/api/clientes', methods=['POST'])
def inserir_cliente():
    data = request.get_json()

    cpf = data.get('cpf')
    nome = data.get('nome')
    email = data.get('email')
    data_nasc = data.get('data_nasc')
    cep = data.get('cep')
    numero_casa = data.get('numero_casa')
    rua = data.get('rua')
    bairro = data.get('bairro')
    cidade = data.get('cidade')
    estado = data.get('estado')

    # verifica se todos os campos obrigatórios foram enviados
    if None in [cpf, nome, email]:
        return jsonify({'error': 'cpf, nome e email são campos obrigatórios'}), 400

    novoCliente = Cliente(cpf=cpf, nome=nome, email=email, data_nasc=data_nasc, cep=cep, numero_casa=numero_casa,
                      rua=rua, bairro=bairro, cidade=cidade, estado=estado)

    try:
        db.session.add(novoCliente)
        db.session.commit()
        
        return jsonify({'message': 'Cliente criado com sucesso'}), 201
    except IntegrityError as e:
        db.session.rollback()

        # verifica se o erro e que ja existe cliente com esse cpf
        if isinstance(e.orig, UniqueViolation):
            return jsonify({'error': f'O cpf {cpf} já existe'}), 400
        else:
            return jsonify({'error': 'Erro ao criar cliente. Erro: ' + str(err)}), 500
    except Exception as err:
        db.session.rollback()
        
        return jsonify({'error': 'Erro ao criar cliente. Erro: ' + str(err)}), 500

"""
    Atualiza um cliente no banco, necessario passar o cpf pela url
    Atualiza apenas os valores que forem passados, ex: se passar nome e email, apenas
    esses serao atualizados
"""
@cliente_bp.route('/api/clientes/<cpf>', methods=['PUT'])
def atualizar_cliente(cpf):
    cliente = Cliente.query.get(cpf)

    if cliente is None:
        return jsonify({'error': 'Cliente não encontrado'}), 404

    data = request.get_json()

    # seta os atributos novos para os valores que foram passados no body (!= None)
    for key in data.keys():
        if data[key] is not None and key in Cliente.__table__.columns.keys():
            setattr(cliente, key, data[key])

    try:
        db.session.commit()

        return jsonify({'message': 'Cliente atualizado com sucesso'}), 200
    except Exception as err:
        db.session.rollback()

        return jsonify({'error': 'Erro ao atualizar cliente. Erro: ' + str(err)}), 500

"""
    Exclui um cliente
    Parametro do body: cpf (cpf do cliente)
"""
@cliente_bp.route('/api/clientes/<cpf>', methods=['DELETE'])
def excluir_cliente(cpf):
    cliente = Cliente.query.get(cpf)

    if cliente is None:
        return jsonify({'error': 'Cliente não encontrado'}), 404

    try:
        db.session.delete(cliente)
        db.session.commit()

        return jsonify({'message': 'Cliente excluído com sucesso'}), 200
    except Exception as err:
        db.session.rollback()

        return jsonify({'error': 'Erro ao excluir cliente. Erro: ' + str(err)}), 500