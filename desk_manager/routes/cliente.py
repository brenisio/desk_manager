import uuid
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from datetime import datetime
from desk_manager.models import Cliente, Reserva
from desk_manager.forms.cadastro import FormCadastroCliente
from desk_manager.extensions import db


CLIENTE = Blueprint('cliente', __name__)

@CLIENTE.route('/cadastro_cliente', methods=['GET', 'POST'])
def cadastrar_cliente():
    form_cadastro_cliente = FormCadastroCliente()
    if form_cadastro_cliente.validate_on_submit():
        id = uuid.uuid4().hex[:8]

        # verificar cpf
        cpf = form_cadastro_cliente.cpf.data
        cliente = Cliente.query.filter_by(cpf=cpf).first()
        if cliente:
            flash('CPF já cadastrado!', 'alert alert-danger')
            return redirect(url_for('cliente.cadastrar_cliente'))

        cliente = Cliente(
            id = id,
            nome = form_cadastro_cliente.nome.data,
            cpf = form_cadastro_cliente.cpf.data,
            telefone = form_cadastro_cliente.telefone.data,
            saldo = 1
        )
        db.session.add(cliente)
        db.session.commit()
        flash('Cliente cadastrado com sucesso!', 'alert alert-success')
        return redirect(url_for('home.home'))
    return render_template('cadastro_cliente.html', form_cadastro_cliente=form_cadastro_cliente)


@CLIENTE.route('/clientes')
def lista_clientes():
    agora = datetime.utcnow()
    if agora.day == 1:
        clientes = Cliente.query.all()
        for cliente in clientes:
            cliente.saldo = 1
        db.session.commit()
    clientes = Cliente.query.all()
    clientes_dict = [cliente.to_dict() for cliente in clientes]
    cliente = Cliente.query.get('1ffe3bb2')
    #print(cliente.plano.nome_do_plano)
    return render_template('lista_clientes.html', clientes=clientes_dict)


@CLIENTE.route('/cliente/<string:cliente_id>/editar', methods=['GET', 'POST'])
def editar_cliente(cliente_id):
    # Busca o cliente do banco de dados pelo ID
    cliente = Cliente.query.get_or_404(cliente_id)

    # Inicializa o formulário com os dados atuais do cliente
    form = FormCadastroCliente(obj=cliente)

    # Verifica se o formulário foi submetido e se é válido
    if form.validate_on_submit():
        if cliente.nome == form.nome.data and cliente.cpf == form.cpf.data and cliente.telefone == form.telefone.data:
            flash('Nenhum dado foi alterado.', 'alert alert-warning')
            return redirect(url_for('cliente.lista_clientes'))

        # Atualiza os dados do cliente com os valores do formulário
        cliente.nome = form.nome.data
        cliente.cpf = form.cpf.data
        cliente.telefone = form.telefone.data

        # Salva as alterações no banco de dados
        db.session.commit()

        # Exibe uma mensagem de sucesso
        flash('Cliente atualizado com sucesso!', 'success')

        # Redireciona para a lista de clientes ou outra página adequada
        return redirect(url_for('cliente.lista_clientes'))

    # Renderiza o template de edição, passando o formulário e o cliente
    return render_template('editar_cliente.html', form_cadastro_cliente=form, cliente=cliente)
@CLIENTE.route('/cliente/<string:cliente_id>/excluir', methods=['POST'])
def excluir_cliente(cliente_id):

    #ADD AQUI A CONDIÇÃO DE VERIFICAR SE O CLIENTE TEVE OU TEM UMA RESERVA

    cliente = Cliente.query.get(cliente_id)

    for reserva in Reserva.query.all():
        if (reserva.cliente == cliente) and (reserva.estado == 1 or reserva.estado == 3):
            flash("Não possível excluir clientes que tenham uma reserva", 'warning')
            return redirect(url_for('cliente.lista_clientes'))

    db.session.delete(cliente)
    db.session.commit()
    return redirect(url_for('cliente.lista_clientes'))

@CLIENTE.route('/buscar_cliente/<string:cpf>', methods=['GET'])
def buscar_cliente_por_cpf(cpf):
    cliente = Cliente.query.filter_by(cpf=cpf).first()
    if not cliente:
        return render_template('lista_clientes.html', cliente_escolhido=None)
    cliente_escolhido = cliente.to_dict()
    print(cliente_escolhido['cpf'])
    return render_template('lista_clientes.html', cliente_escolhido=cliente_escolhido)
