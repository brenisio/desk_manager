import sqlalchemy as sa
import sqlalchemy.orm as so
from desk_manager.extensions import db
from datetime import datetime
import uuid


def generate_hex_id():
    return uuid.uuid4().hex[:8]

class Cliente(db.Model):
    id: so.Mapped[str] = so.mapped_column(sa.String, primary_key=True, default=generate_hex_id)
    nome: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)
    cpf: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)
    telefone: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)
    tipo_plano: so.Mapped[str] = so.mapped_column(sa.Integer, nullable=True)
    # tipo_plano: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey("plano.id", name="fk_plano"), nullable=True)
    saldo: so.Mapped[int] = so.mapped_column(sa.Integer,nullable=True, default=0)
    data_cadastro: so.Mapped[datetime] = so.mapped_column(sa.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'telefone': self.telefone,
            'tipo_plano': self.tipo_plano if self.tipo_plano else 'Sem plano',
            'saldo': self.saldo,
            'data_cadastro': self.data_cadastro.strftime('%d/%m/%Y')
        }

class Mesa(db.Model):
    id: so.Mapped[str] = so.mapped_column(sa.String, primary_key=True, default=generate_hex_id)
    numero: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'numero': self.numero
        }

class Plano(db.Model):
    id: so.Mapped[str] = so.mapped_column(sa.String, primary_key=True, default=generate_hex_id)
    nome_do_plano: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)
    quantidade_de_usos: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)

    def to_dict(self):
        return{
            'id': self.id,
            'nome_do_plano': self.nome_do_plano,
            'quantidade_de_usos': self.quantidade_de_usos
        }
