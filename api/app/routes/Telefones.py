from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from app import db

from app.models.Telefones import Telefones

telefones_bp = Blueprint('telefones', __name__)

"""
    Lista todos os telefones cadastrados no sistema
"""
@telefones_bp.route('/api/telefones', methods=['GET'])
def listar_telefones():
    telefones = Telefones.query.all()

    return jsonify([telefone.as_dict() for telefone in telefones])

"""
    Lista todos os telefones de um cliente
    identificado pelo seu cpf
    Parametro do url: cpf (cpf do cliente)
"""
@telefones_bp.route('/api/telefones/<cpf>', methods=['GET'])
def obter_telefone_cpf(cpf):
    telefones = Telefones.query.filter(Telefones.cliente_tel.like(cpf)).all()

    if len(telefones) <= 0:
        return jsonify({'message': "Telefone(s) não encontrado(s)."})
    
    return jsonify([telefone.as_dict() for telefone in telefones]), 200

"""
    Insere um telefone
    Parametros obrigatorios do body: cliente_tel (cpf do cliente) e telefone
"""
@telefones_bp.route('/api/telefones', methods=['POST'])
def inserir_telefone():
    data = request.get_json()

    cliente_tel = data.get('cliente_tel')
    telefone = data.get('telefone')

    # verifica se todos os campos obrigatórios foram passados
    if not cliente_tel or not telefone:
        return jsonify({'error': 'cliente_tel e telefone são campos obrigatórios'}), 400

    novo_telefone = Telefones(cliente_tel=cliente_tel, telefone=telefone)

    try:
        db.session.add(novo_telefone)
        db.session.commit()

        return jsonify({'message': 'Telefone inserido com sucesso'}), 201
    except IntegrityError as e:

        # verifica se o erro e que ja existe telefone para esse cliente 
        if isinstance(e.orig, UniqueViolation):
            return jsonify({'error': f'O telefone {telefone} para o cliente {cliente_tel} já existe'}), 400
        return jsonify({'error': f'O cliente com cpf {cliente_tel} não existe'}), 500
    except Exception as e:
        db.session.rollback()

        return jsonify({'error': 'Erro ao inserir telefone. Detalhes: ' + str(e)}), 500

"""
    atualiza um telefone
    parametro do url: tel_antigo -> telefone antigo para ser atualizado
    parametros obrigatorios do body: cliente_tel (cpf do cliente) e telefone
"""
@telefones_bp.route('/api/telefones/<tel_antigo>', methods=['PUT'])
def atualiza_telefone(tel_antigo):
    data = request.get_json()

    cliente_tel = data.get("cliente_tel")
    tel_novo = data.get("telefone")

    # verifica se foram passados os campos necessarios para atualizar
    if None in [cliente_tel, tel_novo, tel_antigo]:
        return jsonify({'error': "É necessário mandar o telefone novo, o antigo (url) e o cpf do cliente"}), 400
    
    telefone = Telefones.query.get((cliente_tel, tel_antigo))

    if telefone is None:
        return jsonify({'error': 'Telefone não enconrtado'}), 500
    
    setattr(Telefones,"cliente_tel", cliente_tel)
    setattr(Telefones,"telefone", tel_novo)
    
    try:
        db.session.commit()

        return jsonify({"message": "Telefone atualizado com sucesso"}), 200
    except Exception as e:
        db.session.rollback()

        return jsonify({'error': 'Erro ao atualizar Telefone. Detalhes: ' + str(e)}), 500

"""
    Exclui um telefone
    Parametros da url: cliente_tel (cpf do cliente) e telefone
"""
@telefones_bp.route('/api/telefones/<cliente_tel>/<telefone>', methods=['DELETE'])
def excluir_telefone(cliente_tel, telefone):
    telefone = Telefones.query.get((cliente_tel, telefone))

    if telefone is None:
        return jsonify({'error': 'Telefone não encontrado'}), 404

    try:
        db.session.delete(telefone)
        db.session.commit()

        return jsonify({'message': 'Telefone excluído com sucesso'}), 200
    except Exception as e:
        db.session.rollback()

        return jsonify({'error': 'Erro ao excluir telefone. Detalhes: ' + str(e)}), 500