# config.py
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Configurações do banco de dados
DATABASE = 'db'
DB_USERNAME = 'fellip'
DB_PASSWORD = 'fellip'
DB_HOST = 'localhost'
DB_PORT = 5432

# Configuração do SQLAlchemy
SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DATABASE}'
SQLALCHEMY_TRACK_MODIFICATIONS = False