import sqlalchemy as sa
import sqlalchemy.orm as so
from desk_manager.extensions import db
from datetime import datetime
import uuid
import enum


def generate_hex_id():
    return uuid.uuid4().hex[:8]


class Cliente(db.Model):
    __tablename__ = 'cliente'

    id: so.Mapped[str] = so.mapped_column(sa.String, primary_key=True, default=generate_hex_id)
    nome: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)
    cpf: so.Mapped[str] = so.mapped_column(sa.String, unique=True, nullable=False)
    telefone: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)
      
    # Mantemos o tipo_plano_id como ForeignKey
    tipo_plano_id: so.Mapped[str] = so.mapped_column(sa.String, sa.ForeignKey("plano.id"), nullable=True)

    # O relacionamento com a classe Plano
    plano: so.Mapped["PlanoDeUso"] = so.relationship("PlanoDeUso", back_populates="clientes")

    reservas: so.Mapped[list["Reserva"]] = so.relationship("Reserva", back_populates="cliente")

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

    @classmethod
    def buscar_todos_clientes(cls):

        return cls.query.all()

    @classmethod
    def buscar_cliente_por_id(cls, cliente_id):

        return cls.query.get(cliente_id)

    @classmethod
    def buscar_cliente_por_cpf(cls,cpf):

        return cls.query.filter_by(cpf=cpf).first()


class Mesa(db.Model):
    id: so.Mapped[str] = so.mapped_column(sa.String, primary_key=True, default=generate_hex_id)
    numero: so.Mapped[str] = so.mapped_column(sa.String, unique=True, nullable=False)

    reservas: so.Mapped[list["Reserva"]] = so.relationship("Reserva", back_populates="mesa")

    def to_dict(self):
        return {
            'id': self.id,
            'numero': self.numero
        }

    @classmethod
    def buscar_mesa_por_id(cls, mesa_id):

        return cls.query.get(mesa_id)

    @classmethod
    def buscar_mesa_por_numero(cls, numero):

        return cls.query.filter_by(numero=numero).first()

    @classmethod
    def buscar_todas_mesas(cls):

        return cls.query.all()


class PlanoDeUso(db.Model):
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

    @classmethod
    def buscar_todos_planos(cls):

        return cls.query.all()

    @classmethod
    def buscar_plano_por_nome(cls, nome_do_plano):

        return cls.query.filter_by(nome_do_plano=nome_do_plano).first()

    @classmethod
    def buscar_plano_por_id(cls, plano_id):

        return cls.query.get(plano_id)


class EstadoReserva(enum.IntEnum):
    RESERVADA = 1
    CANCELADA = 2
    EM_USO = 3
    FINALIZADA = 4


class PeriodoReserva(enum.IntEnum):
    MANHA = 1
    TARDE = 2
    NOITE = 3


class Reserva(db.Model):
    id: so.Mapped[str] = so.mapped_column(sa.String, primary_key=True, default=generate_hex_id)
    codigo: so.Mapped[str] = so.mapped_column(sa.String, unique=True ,nullable=False)
    data: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=False)
    periodo: so.Mapped[PeriodoReserva] = so.mapped_column(sa.Integer, nullable=False)
    estado: so.Mapped[EstadoReserva] = so.mapped_column(sa.Integer, nullable=False, default=EstadoReserva.RESERVADA)
    data_chegada: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=True)
    data_saida: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=True)
    data_cancelamento: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=True)

    cliente: so.Mapped[Cliente] = so.relationship(Cliente, back_populates="reservas")
    cliente_id: so.Mapped[str] = so.mapped_column(sa.String, sa.ForeignKey("cliente.id"), nullable=False)

    mesa: so.Mapped[Mesa] = so.relationship(Mesa, back_populates="reservas")
    mesa_id: so.Mapped[str] = so.mapped_column(sa.String, sa.ForeignKey("mesa.id"), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'data': self.data.strftime('%d/%m/%Y'),
            'periodo': PeriodoReserva(self.periodo).name,
            'estado': EstadoReserva(self.estado).name,
            'cliente': self.cliente,
            'mesa': self.mesa
        }

    @classmethod
    def buscar_todas_reservas(cls):

        return cls.query.all()

    @classmethod
    def buscar_reserva_por_codigo(cls, codigo):

        return cls.query.filter_by(codigo=codigo).first()

    @classmethod
    def buscar_reserva_por_id(cls, reserva_id):

        return cls.query.get_or_404(reserva_id)
