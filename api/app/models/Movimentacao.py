from sqlalchemy import CheckConstraint
from app import db
from sqlalchemy.orm import backref

class Movimentacao(db.Model):
    __tablename__ = 'movimentacao'

    data_hora = db.Column(db.TIMESTAMP, primary_key=True)
    conta_mov = db.Column(db.BigInteger, db.ForeignKey('conta.numero'), primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(1), nullable=False)
    # Adicionar a restrição CHECK usando o CheckConstraint
    __table_args__ = (
        CheckConstraint("tipo IN ('d', 's')", name="check_tipo_movimentacao"),
    )

    conta = db.relationship('Conta', backref=backref("movimentacoes", cascade="all, delete-orphan"), lazy=True)

    def __repr__(self):
        return f'Movimentacao(data_hora={self.data_hora}, conta_mov={self.conta_mov}, valor={self.valor}, tipo={self.tipo})'
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}