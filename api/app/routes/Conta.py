from flask import Blueprint, jsonify, request
from execute_query import execute_query
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, or_, not_
from app import db

from app.models.Conta import Conta

conta_bp = Blueprint('conta', __name__)

"""
    Rota de contas que retorna todas as contas presentes no banco de dados
"""
@conta_bp.route('/api/contas', methods=['GET'])
def listar_clientes():
    contas = Conta.query.all()

    return jsonify([c.as_dict() for c in contas])

"""
    Rota de contas que retorna apenas uma conta:
    Parâmetro de url: parametro -> numero da conta ou cpf do usuário
    no caso da busca pelo cpf do usuário o retorno pode ser mais de uma conta
"""
@conta_bp.route('/api/contas/<parametro>', methods=['GET'])
def obter_conta_parametro_url(parametro):
    parametro_int = None
    try:
        parametro_int = int(parametro)
    except ValueError:
        pass

    contas = Conta.query.filter(or_(Conta.numero == parametro_int, Conta.cliente_conta.like(parametro))).all()

    if len(contas) <= 0:
        return jsonify({'error': "Conta(s) não encontrada."})
    
    return jsonify([conta.as_dict() for conta in contas]), 200

"""
    Cria uma conta e salva no banco de dados
    Campos obrigatórios no body: numero, cliente_conta (cpf do dono da conta), saldo
"""
@conta_bp.route('/api/contas', methods=['POST'])
def inserir_conta():
    data = request.get_json()

    numero = data.get('numero')
    cliente_conta = data.get('cliente_conta')
    saldo = data.get('saldo')
    limite_mov = data.get('limite_mov')
    senha = data.get('senha')

    # Verificar se todos os campos obrigatórios foram fornecidos
    if None in [numero, cliente_conta, saldo, senha]:
        return jsonify({'error': 'numero, cliente_conta, saldo e senha são campos obrigatórios'}), 400

    conta = Conta(numero=numero, cliente_conta=cliente_conta, saldo=saldo, limite_mov=limite_mov, senha=senha)

    try:
        db.session.add(conta)
        db.session.commit()
        return jsonify({'message': 'Conta criada com sucesso'}), 201
    except IntegrityError:
        return jsonify({'error': f'O cliente com cpf {cliente_conta} não existe'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao criar conta. Detalhes: ' + str(e)}), 500

"""
    Atualiza uma conta no banco de dados
    Necessário passar o número da conta que será atualizada
    Atualiza apenas os valores passados
"""
@conta_bp.route('/api/contas/<numero>', methods=['PUT'])
def atualizar_conta(numero):
    conta = Conta.query.get(numero)

    if conta is None:
        return jsonify({'error': 'Conta não encontrada'}), 400

    data = request.get_json()

    # Seta os atributos novos para os valores que foram passados no body (!= None)
    for key in data.keys():
        if data[key] is not None and key in Conta.__table__.columns.keys():
            setattr(conta, key, data[key])

    try:
        db.session.commit()
        return jsonify({'message': 'Conta atualizada com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao atualizar conta. Detalhes: ' + str(e)}), 500

"""
    Exclui uma conta
    Parâmetro do url: numero (numero da conta)
"""
@conta_bp.route('/api/contas/<numero>', methods=['DELETE'])
def excluir_conta(numero):
    conta = Conta.query.get(numero)

    if conta is None:
        return jsonify({'error': 'Conta não encontrada'}), 404

    try:
        db.session.delete(conta)
        db.session.commit()
        return jsonify({'message': 'Conta excluída com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao excluir conta. Detalhes: ' + str(e)}), 500
