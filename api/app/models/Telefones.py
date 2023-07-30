from app import db

class Telefones(db.Model):
    __tablename__ = 'telefones'

    cliente_tel = db.Column(db.String(14), db.ForeignKey('cliente.cpf', ondelete='CASCADE'), primary_key=True)
    telefone = db.Column(db.String(11), primary_key=True)

    cliente = db.relationship('Cliente', backref='telefones', lazy=True)

    def __repr__(self):
        return f"Telefone(cliente_tel={self.cliente_tel}, telefone={self.telefone})"
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}