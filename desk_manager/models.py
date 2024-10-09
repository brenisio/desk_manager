import sqlalchemy as sa
import sqlalchemy.orm as so
from desk_manager.extensions import db
from datetime import datetime
import uuid


def generate_hex_id():
    return uuid.uuid4().hex[:8]


class Cliente(db.Model):
    __tablename__ = 'cliente'

    id: so.Mapped[str] = so.mapped_column(sa.String, primary_key=True, default=generate_hex_id)
    nome: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)
    cpf: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)
    telefone: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)

    # Mantemos o tipo_plano_id como ForeignKey
    tipo_plano_id: so.Mapped[str] = so.mapped_column(sa.String, sa.ForeignKey("plano.id"), nullable=True)

    # O relacionamento com a classe Plano
    plano: so.Mapped["Plano"] = so.relationship("Plano", back_populates="clientes")

    saldo: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'telefone': self.telefone,
            'plano': self.plano.nome_do_plano if self.plano else None,  # Referência ao plano
            'saldo': self.saldo,
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
    __tablename__ = 'plano'

    id: so.Mapped[str] = so.mapped_column(sa.String, primary_key=True, default=generate_hex_id)
    nome_do_plano: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)
    quantidade_de_usos: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)

    # Relacionamento com Cliente
    clientes: so.Mapped[list["Cliente"]] = so.relationship("Cliente", back_populates="plano")

    def to_dict(self):
        return {
            'id': self.id,
            'nome_do_plano': self.nome_do_plano,
            'quantidade_de_usos': self.quantidade_de_usos
        }