#from crypt import methods

from desk_manager.models import PlanoDeUso
from flask import Blueprint, render_template, request, redirect, url_for, flash
from desk_manager.extensions import db
from desk_manager.routes.reserva import Reserva, RESERVA
import uuid

REGISTROS = Blueprint('registros', __name__)

@REGISTROS.route('/registros')
def listagem():
    reservas = Reserva.query.all()
    reservas_dict = [reserva.to_dict() for reserva in reservas]
    return render_template('listagem_registros.html', reservas=reservas_dict)


@REGISTROS.route('/registrar_chegada')
def registrar_chegada():
    return None


@REGISTROS.route('/registrar_saida')
def registrar_saida():
    return None


@REGISTROS.route('/registrar_cancelamento')
def registrar_cancelamento():
    return None

@REGISTROS.route('/buscar_listagem', methods=['GET'])
def buscar_listagem_por_codigo(codigo):
    reserva = Reserva.query.filter_by(codigo=codigo).first()
    if not reserva:
        return render_template('listagem_registros.html', reserva_escolhida=None)
    return render_template('listagem_registros.html', reserva_escolhida=reserva.to_dict())
