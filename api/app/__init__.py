# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

db = SQLAlchemy(app)

# Importar rotas
from app.routes.Cliente import cliente_bp
app.register_blueprint(cliente_bp)

from app.routes.Conta import conta_bp
app.register_blueprint(conta_bp)

from app.routes.Telefones import telefones_bp
app.register_blueprint(telefones_bp)

from app.routes.Movimentacao import movimentacao_bp
app.register_blueprint(movimentacao_bp)