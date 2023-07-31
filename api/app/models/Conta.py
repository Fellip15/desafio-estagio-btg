from app import db
from sqlalchemy.orm import backref

class Conta(db.Model):
    __tablename__ = 'conta'

    numero = db.Column(db.BigInteger, primary_key=True)
    cliente_conta = db.Column(db.String(14), db.ForeignKey('cliente.cpf'), nullable=False)
    saldo = db.Column(db.Float, nullable=False)
    limite_mov = db.Column(db.Float)
    senha = db.Column(db.String(32), nullable=False)

    cliente = db.relationship('Cliente', backref=backref("contas", cascade="all, delete-orphan"))

    def __repr__(self):
        return f"Conta(numero={self.numero}, cliente_conta='{self.cliente_conta}', " \
               f"saldo={self.saldo}, limite_mov={self.limite_mov}, senha='{self.senha}')"
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}