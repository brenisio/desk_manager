import uuid
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from datetime import datetime
from desk_manager.models import Cliente
from desk_manager.forms.cadastro import FormCadastroCliente
from desk_manager.extensions import db


CLIENTE = Blueprint('cliente', __name__)

@CLIENTE.route('/cadastro_cliente', methods=['GET', 'POST'])
def cadastrar_cliente():
    form_cadastro_cliente = FormCadastroCliente()
    if form_cadastro_cliente.validate_on_submit():
        id = uuid.uuid4().hex[:8]

        cliente = Cliente(
            id = id,
            nome = form_cadastro_cliente.nome.data,
            cpf = form_cadastro_cliente.cpf.data,
            telefone = form_cadastro_cliente.telefone.data,
            data_cadastro = datetime.now(),
        )
        db.session.add(cliente)
        db.session.commit()
        flash('Cliente cadastrado com sucesso!', 'alert alert-success')
        return redirect(url_for('home.home'))
    return render_template('cadastro_cliente.html', form_cadastro_cliente=form_cadastro_cliente)

@CLIENTE.route('/clientes')
def lista_clientes():
    clientes = Cliente.query.all()
    clientes_dict = [cliente.to_dict() for cliente in clientes]
    return render_template('lista_clientes.html', clientes=clientes_dict)

@CLIENTE.route('/cliente/<string:cliente_id>/editar', methods=['GET'])
def editar_cliente(cliente_id):
    cliente = Cliente.query.get(cliente_id)
    return render_template('editar_cliente.html', cliente=cliente)

@CLIENTE.route('/cliente/<string:cliente_id>/editar', methods=['POST'])
def atualizar_cliente(cliente_id):
    cliente = Cliente.query.get(cliente_id)
    cliente.nome = request.form['nome']
    cliente.cpf = request.form['cpf']
    cliente.telefone = request.form['telefone']
    db.session.commit()
    return redirect(url_for('cliente.lista_clientes'))

@CLIENTE.route('/cliente/<string:cliente_id>/excluir', methods=['POST'])
def excluir_cliente(cliente_id):
    cliente = Cliente.query.get(cliente_id)
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
