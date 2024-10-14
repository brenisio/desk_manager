from desk_manager.models import Reserva, Cliente, Mesa, PeriodoReserva
from flask import Blueprint, render_template, request, redirect, url_for, flash
from desk_manager.extensions import db
from desk_manager.forms.cadastro import FormCadastroReserva
import uuid
from datetime import datetime, date

RESERVA = Blueprint('reserva', __name__)

@RESERVA.route('/reservas')
def lista_reservas():
    reservas = Reserva.query.all()
    reservas_dict = [reserva.to_dict() for reserva in reservas]
    return render_template('lista_reservas.html', reservas=reservas_dict)

@RESERVA.route('/reserva/<string:reserva_id>/editar', methods=['GET', 'POST'])
def editar_reserva(reserva_id):
    reserva = Reserva.query.get_or_404(reserva_id)

    form_editar_reserva = FormCadastroReserva()

    if form_editar_reserva.validate_on_submit():


        cpf_cliente = form_editar_reserva.cpf_cliente.data  # cpf do cliente do formulário
        numero_mesa = form_editar_reserva.numero_mesa.data  # numero da mesa do formulário

        cliente = db.session.query(Cliente).filter_by(cpf=cpf_cliente).first()
        mesa = db.session.query(Mesa).filter_by(numero=numero_mesa).first()

        if not cliente:
            flash('Cliente não encontrado.', 'warning')
            return redirect(url_for('reserva.cadastrar_reserva'))
        if not mesa:
            flash('Mesa não encontrada.', 'warning')
            return redirect(url_for('reserva.cadastrar_reserva'))

        data_reserva = form_editar_reserva.data.data
        data_formatada = data_reserva.strftime("%d%m%Y")

        periodo_reserva_value = int(form_editar_reserva.periodo.data)
        periodo_reserva = PeriodoReserva(periodo_reserva_value)

        # Verifica se data e periodo da reserva são válidos
        if data_reserva < datetime.now():
            flash('Data inválida.', 'warning')
            return redirect(url_for('reserva.cadastrar_reserva'))
        for reserva_bd in Reserva.query.all():
            if (data_reserva == reserva_bd.data and
                periodo_reserva_value == reserva_bd.periodo and
                mesa == reserva_bd.mesa and
                reserva_bd.estado != 2):
                flash('Já existe uma reseva neste período.', 'warning')
                return redirect(url_for('reserva.cadastrar_reserva'))

        codigo_reserva = str(data_formatada) + str(periodo_reserva) + str(numero_mesa)
        reserva.codigo = codigo_reserva
        reserva.data = data_reserva
        reserva.periodo = PeriodoReserva(periodo_reserva)
        cliente = cliente
        mesa = mesa

        db.session.commit()

        flash('Reserva atualizada com sucesso!', 'success')

        # Redireciona para a lista de clientes ou outra página adequada
        return redirect(url_for('reserva.lista_reservas'))

    # Renderiza o template de edição, passando o formulário e o cliente
    return render_template('editar_reserva.html', form_editar_reserva=form_editar_reserva, reserva=reserva)

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

        # Verifica se cliente e mesa são válidos
        if not cliente:
            flash('Cliente não encontrado.', 'warning')
            return redirect(url_for('reserva.cadastrar_reserva'))
        if not mesa:
            flash('Mesa não encontrada.', 'warning')
            return redirect(url_for('reserva.cadastrar_reserva'))
        
        # Verifica se o cliente tem saldo para reservar
        if cliente.saldo < 1:
            flash('Cliente não tem saldo suficiente', 'warning')
            return redirect(url_for('reserva.cadastrar_reserva'))

        data_reserva = form_cadastro_reserva.data.data
        data_formatada = data_reserva.strftime("%d%m%Y")

        periodo_reserva_value = int(form_cadastro_reserva.periodo.data)
        periodo_reserva = PeriodoReserva(periodo_reserva_value)

        # Verifica se data e periodo da reserva são válidos
        if data_reserva < datetime.now():
            flash('Data inválida.', 'warning')
            return redirect(url_for('reserva.cadastrar_reserva'))
        
        for reserva_bd in Reserva.query.all():

            if (cliente == reserva_bd.cliente and
                data_reserva == reserva_bd.data and
                periodo_reserva_value == reserva_bd.periodo and
                reserva_bd.estado != 2):
                flash('O cliente já tem outra reserva nesse período.', 'warning')
                return redirect(url_for('reserva.cadastrar_reserva'))

            if (data_reserva == reserva_bd.data and
                periodo_reserva_value == reserva_bd.periodo and
                mesa == reserva_bd.mesa and
                reserva_bd.estado != 2):
                flash('A mesa já está resevada neste período.', 'warning')
                return redirect(url_for('reserva.cadastrar_reserva'))
        
        # Define o código (data + digito do periodo + numero da mesa)
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
        flash('Reserva cadastrada com sucesso!', 'alert-success')
        return redirect(url_for('home.home'))
    return render_template('cadastro_reserva.html', form_cadastro_reserva=form_cadastro_reserva)



