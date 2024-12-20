from desk_manager.models import PlanoDeUso, EstadoReserva
from flask import Blueprint, render_template, request, redirect, url_for, flash
from desk_manager.extensions import db
from desk_manager.routes.reserva import Reserva, RESERVA, buscar_reserva_por_codigo
from datetime import datetime, timedelta, time
from sqlalchemy import func
import uuid

REGISTROS = Blueprint('registros', __name__)

@REGISTROS.route('/registros')
def listagem():
    reservas = buscar_reservas_hoje()
    reservas_dict = [reserva.to_dict() for reserva in reservas]
    return render_template('listagem_registros.html', reservas=reservas_dict)


@REGISTROS.route('/reservas/<string:reserva_id>/registrar_chegada', methods=['POST'])
def registrar_chegada(reserva_id):
    reserva = Reserva.buscar_reserva_por_id(reserva_id)
    hoje = datetime.now().date()

    if reserva.data == hoje:
        if reserva.estado == EstadoReserva.RESERVADA:
            reserva.data_chegada = datetime.now()
            reserva.estado = EstadoReserva.EM_USO
            db.session.commit()
            flash("Chegada registrada com sucesso!", "success")
            return redirect(url_for('registros.listagem', reserva_id=reserva.id))
        else:
            flash("Só pode se registrar entrada caso o estado seja Reservada", "warning")
            return  redirect(url_for('registros.listagem', reserva_id=reserva.id))
    else:
        flash(f"Só se pode registrar chegada de uma reserva de hoje {hoje}", "warning")
        return redirect(url_for('registros.listagem', reserva_id=reserva.id))

@REGISTROS.route('/reservas/<string:reserva_id>/registrar_saida', methods=['POST'])
def registrar_saida(reserva_id):
    reserva = Reserva.buscar_reserva_por_id(reserva_id)
    hoje = datetime.now().date()

    if reserva.data == hoje:
        if reserva.estado == EstadoReserva.EM_USO:
            reserva.data_saida = datetime.now()
            reserva.estado = EstadoReserva.FINALIZADA
            db.session.commit()
            flash("Saída registrada com sucesso!", "success")
            return redirect(url_for('registros.listagem', reserva_id=reserva.id))
        else:
            flash("Só pode se registrar saída caso a reserva esteja em uso", "warning")
            return  redirect(url_for('registros.listagem', reserva_id=reserva.id))
    else:
        flash(f"Só se pode registrar saída de uma reserva de hoje {hoje}", "warning")
        return redirect(url_for('registros.listagem', reserva_id=reserva.id))


@REGISTROS.route('/reservas/<string:reserva_id>/registrar_cancelamento', methods=['POST'])
def registrar_cancelamento(reserva_id):
    reserva = Reserva.buscar_reserva_por_id(reserva_id)
    hoje = datetime.now()

    if reserva.estado == EstadoReserva.RESERVADA:
        if reserva.data > hoje + timedelta(days=1):
            reserva.data_cancelamento = datetime.now()
            reserva.estado = EstadoReserva.CANCELADA
            db.session.commit()
            flash("Cancelamento registrado com sucesso!", "warning")
        else:
            flash("O cancelamento só pode ser feito até 24 horas antes da data da reserva.", "warning")
            return redirect(url_for('registros.listagem', reserva_id=reserva.id))
    else:
        flash("Só pode se cancelar uma reserva que ainda não foi iniciada", "warning")
        return redirect(url_for('registros.listagem', reserva_id=reserva.id))
    return  redirect(url_for('registros.listagem', reserva_id=reserva.id))

@REGISTROS.route('/buscar_listagem/<string:codigo>', methods=['GET'])
def buscar_listagem_por_codigo(codigo):
    reserva = Reserva.buscar_reserva_por_codigo(codigo)
    if not reserva:
        return render_template('listagem_registros.html', reserva_escolhida=None)
    return render_template('listagem_registros.html', reserva_escolhida=reserva.to_dict())

def buscar_reservas_hoje():
    hoje = datetime.now().date()

    return Reserva.query.filter(func.date(Reserva.data) == hoje).all()
