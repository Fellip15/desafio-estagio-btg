from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import CheckViolation
from execute_query import execute_query
from sqlalchemy import and_, or_, not_
from app import db

from app.models.Movimentacao import Movimentacao

movimentacao_bp = Blueprint('movimentacao', __name__)

"""
    Lista todas as movimentações
"""
@movimentacao_bp.route('/api/movimentacoes', methods=['GET'])
def listar_movimentacoes():
    movimentacoes = Movimentacao.query.all()

    return jsonify([movimentacao.as_dict() for movimentacao in movimentacoes])

"""
    Lista as movimentação de uma conta
    parametro de url: conta -> numero da conta
"""
@movimentacao_bp.route('/api/movimentacoes/<int:conta>', methods=['GET'])
def obter_movimentacoes_conta(conta):
    movimentacoes = Movimentacao.query.filter_by(conta_mov=conta).all()

    if len(movimentacoes) <= 0:
        return jsonify({'error': "Telefone(s) não encontrado(s)."})
    
    return jsonify([movimentacao.as_dict() for movimentacao in movimentacoes]), 200

"""
    Cria uma movimentação
    Parâmetros obrigatórios do body: data_hora, conta_mov, valor e tipo
"""
@movimentacao_bp.route('/api/movimentacoes', methods=['POST'])
def inserir_movimentacao():
    data = request.get_json()

    data_hora = data.get('data_hora')
    conta_mov = data.get('conta_mov')
    valor = data.get('valor')
    tipo = data.get('tipo')

    # Verificar se todos os campos obrigatórios foram fornecidos
    if not data_hora or not conta_mov or not valor or not tipo:
        return jsonify({'error': 'data_hora, conta_mov, valor e tipo são campos obrigatórios'}), 400

    nova_movimentacao = Movimentacao(data_hora=data_hora, conta_mov=conta_mov, valor=valor, tipo=tipo)

    try:
        db.session.add(nova_movimentacao)
        db.session.commit()
        return jsonify({'message': 'Movimentação inserida com sucesso'}), 201
    except IntegrityError:
        return jsonify({'error': f'A conta com número {conta_mov} não existe'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao inserir movimentação. Detalhes: ' + str(e)}), 500

"""
    Atualiza uma movimentação
    Parâmetros de url: conta_mov (numero da conta) e data_hora
    parametros obrigatórios do body: valor e tipo
"""
@movimentacao_bp.route('/api/movimentacoes/<data_hora>/<int:conta_mov>', methods=['PUT'])
def atualiza_movimentacao(data_hora, conta_mov):
    data = request.get_json()

    novo_valor = data.get("valor")
    novo_tipo = data.get("tipo")

    if None in [data_hora, conta_mov, novo_valor, novo_tipo]:
        return jsonify({'error': "É necessário mandar a data_hora, conta_mov, novo valor e novo tipo"}), 400
    
    movimentacao = Movimentacao.query.get((data_hora, conta_mov))

    if movimentacao is None:
        return jsonify({'error': 'Movimentação não encontrada'}), 500

    movimentacao.valor = novo_valor
    movimentacao.tipo = novo_tipo
    
    try:
        db.session.commit()
        return jsonify({"message": "Movimentação atualizada com sucesso"}), 200
    except IntegrityError as e:
        db.session.rollback()
        if isinstance(e.orig, CheckViolation):
            return jsonify({'error': f'O tipo deve ser "d" ou "s"'}), 400
        else:
            return jsonify({'error': f'A conta {conta_mov} não existe'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao atualizar movimentação. Detalhes: ' + str(e)}), 500

"""
    Exclui uma movimentação
    Parâmetros da url: data_hora e conta_mov (numero da conta)
"""
@movimentacao_bp.route('/api/movimentacoes/<data_hora>/<conta_mov>', methods=['DELETE'])
def excluir_movimentacao(data_hora, conta_mov):
    movimentacao = Movimentacao.query.get((data_hora, conta_mov))

    if movimentacao is None:
        return jsonify({'error': 'Movimentação não encontrada'}), 404

    try:
        db.session.delete(movimentacao)
        db.session.commit()
        return jsonify({'message': 'Movimentação excluída com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao excluir movimentação. Detalhes: ' + str(e)}), 500
