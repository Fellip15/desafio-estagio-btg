from flask_sqlalchemy import SQLAlchemy

from app import db

class Cliente(db.Model):
    __tablename__ = 'cliente'

    cpf = db.Column(db.String(14), primary_key=True)
    nome = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    data_nasc = db.Column(db.Date)
    cep = db.Column(db.String(9))
    numero_casa = db.Column(db.Integer)
    rua = db.Column(db.String(64))
    bairro = db.Column(db.String(64))
    cidade = db.Column(db.String(64))
    estado = db.Column(db.String(2))

    def __repr__(self):
        return f"Cliente(cpf={self.cpf}, nome='{self.nome}', email='{self.email}', " \
               f"data_nasc='{self.data_nasc}', cep='{self.cep}', numero_casa={self.numero_casa}, " \
               f"rua='{self.rua}', bairro='{self.bairro}', cidade='{self.cidade}', estado='{self.estado}')"
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}