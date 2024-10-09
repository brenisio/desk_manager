from desk_manager.models import Reserva, Cliente, Mesa, PeriodoReserva
from flask import Blueprint, render_template, request, redirect, url_for, flash
from desk_manager.extensions import db
from desk_manager.forms.cadastro import FormCadastroReserva
import uuid

RESERVA = Blueprint('reserva', __name__)

@RESERVA.route('/reservas')
def lista_reservas():
    reservas = Reserva.query.all()
    reservas_dict = [reserva.to_dict() for reserva in reservas]
    return render_template('lista_reservas.html', reservas=reservas_dict)

@RESERVA.route('/reserva/<string:reserva_id>/editar', methods=['GET'])
def editar_reserva(reserva_id):
    reserva = Reserva.query.get(reserva_id)
    return render_template('editar_reserva.html', reserva=reserva)

@RESERVA.route('/reserva/<string:reserva_id>/editar', methods=['POST'])
def atualizar_reserva(reserva_id):
    reserva = Reserva.query.get(reserva_id)
    reserva.codigo = request.form['codigo']
    db.session.commit()
    return redirect(url_for('reserva.lista_reservas'))

@RESERVA.route('/reserva/<string:reserva_id>/excluir', methods=['POST'])
def excluir_reserva(reserva_id):
    reserva = Reserva.query.get(reserva_id)
    db.session.delete(reserva)
    db.session.commit()
    return redirect(url_for('reserva.lista_reservas'))
    

@RESERVA.route('/buscar_reserva/<string:codigo>', methods=['GET'])
def buscar_reserva_por_codigo(codigo):
    reserva = Reserva.query.filter_by(codigo=codigo).first()
    if not reserva:
        return render_template('lista_reservas.html', reserva_escolhida=None)
    return render_template('lista_reservas.html', reserva_escolhida=reserva.to_dict())

@RESERVA.route('/cadastro_reserva', methods=['GET', 'POST'])
def cadastrar_reserva():
    form_cadastro_reserva = FormCadastroReserva()
    if form_cadastro_reserva.validate_on_submit():
        id = uuid.uuid4().hex[:8]

        cpf_cliente = form_cadastro_reserva.cpf_cliente.data  # ID do cliente do formulário
        numero_mesa = form_cadastro_reserva.numero_mesa.data  # ID da mesa do formulário

        cliente = db.session.query(Cliente).filter_by(cpf=cpf_cliente).first()
        mesa = db.session.query(Mesa).filter_by(numero=numero_mesa).first()

        if not cliente or not mesa:
            return "Cliente ou mesa nao encontrado", 400

        data_reserva = form_cadastro_reserva.data.data
        data_formatada = data_reserva.strftime("%d%m%Y")

        periodo_reserva_value = int(form_cadastro_reserva.periodo.data)
        periodo_reserva = PeriodoReserva(periodo_reserva_value)

        codigo_reserva = str(data_formatada) + str(periodo_reserva) + str(numero_mesa)

        reserva = Reserva(
            id = id,
            codigo = codigo_reserva,
            data = data_reserva,
            periodo = PeriodoReserva(periodo_reserva),
            cliente = cliente,
            mesa = mesa
        )

        db.session.add(reserva)
        db.session.commit()
        flash('Mesa cadastrada com sucesso!', 'alert-success')
        return redirect(url_for('home.home'))
    return render_template('cadastro_reserva.html', form_cadastro_reserva=form_cadastro_reserva)
