from urllib.parse import uses_relative

from desk_manager.models import PlanoDeUso, Cliente
from flask import Blueprint, render_template, request, redirect, url_for, flash
from desk_manager.extensions import db
from desk_manager.forms.cadastro import FormCadastroPlano
import uuid


PLANO = Blueprint('plano', __name__)

@PLANO.route('/tipos_planos')
def lista_planos():
    planos = PlanoDeUso.buscar_todos_planos()
    planos_dict = [plano.to_dict() for plano in planos]
    # mostra todos os clientes do plano
    # plano = PlanoDeUso.query.get('8c2bbf09')
    #for cliente in plano.clientes:
        #print(cliente.nome)
    return render_template('lista_planos.html', planos=planos_dict, plano_escolhido=None)


@PLANO.route('/plano/<string:plano_id>/editar', methods=['GET', 'POST'])
def editar_plano(plano_id):
    plano = PlanoDeUso.buscar_plano_por_id(plano_id)
    form = FormCadastroPlano(obj=plano)

    if form.validate_on_submit():
        nome_do_plano = form.nome_do_plano.data
        if nome_do_plano != plano.nome_do_plano:
            nome_repetido = PlanoDeUso.query.filter_by(nome_do_plano=nome_do_plano).first()
            if nome_repetido:
                flash('Já existe um plano com este nome!', 'warning')
                return redirect(url_for('plano.lista_planos'))

        if plano.nome_do_plano == form.nome_do_plano.data and plano.quantidade_de_usos == form.quantidade_de_usos.data:
            flash(f'Nenhuma informação do plano {form.nome_do_plano.data} foi alterada!', 'warning')
            return redirect(url_for('plano.lista_planos'))

        plano.nome_do_plano = form.nome_do_plano.data
        plano.quantidade_de_usos = form.quantidade_de_usos.data

        db.session.commit()

        flash('Plano atualizado com sucesso!', 'success')

        return redirect(url_for('plano.lista_planos'))

    return render_template('editar_planos.html', form_cadastro_plano=form, plano=plano)


@PLANO.route('/plano/<string:plano_id>/editar', methods=['POST'])
def atualizar_plano(plano_id):
    plano = PlanoDeUso.buscar_plano_por_id(plano_id)
    plano.nome_do_plano = request.form['nome_do_plano']
    plano.quantidade_de_usos = request.form['quantidade_de_usos']
    db.session.commit()
    return redirect(url_for('plano.lista_planos'))


@PLANO.route('/plano/<string:plano_id>/excluir', methods=['POST'])
def excluir_plano(plano_id):
    plano = PlanoDeUso.buscar_plano_por_id(plano_id)
    db.session.delete(plano)
    db.session.commit()
    return redirect(url_for('plano.lista_planos'))


@PLANO.route('/buscar_plano/<string:nome_do_plano>', methods=['GET'])
def buscar_plano_por_nome(nome_do_plano):
    plano = PlanoDeUso.buscar_plano_por_nome(nome_do_plano)
    if not plano:
        return render_template('lista_planos.html', plano_escolhido=None)
    plano_escolhido = plano.to_dict()
    return render_template('lista_planos.html', plano_escolhido=plano_escolhido)


@PLANO.route('/cadastro_plano', methods=['GET', 'POST'])
def cadastrar_plano():
    form_cadastro_plano = FormCadastroPlano()
    if form_cadastro_plano.validate_on_submit():
        id = uuid.uuid4().hex[:8]

        nome_do_plano = form_cadastro_plano.nome_do_plano.data
        plano = PlanoDeUso.query.filter_by(nome_do_plano=nome_do_plano).first()
        if plano:
            flash('Plano com o mesmo nome informado existente, atenção!', 'warning')
            return redirect(url_for('plano.lista_planos'))

        plano = PlanoDeUso(
            id=id,
            nome_do_plano=form_cadastro_plano.nome_do_plano.data,
            quantidade_de_usos=form_cadastro_plano.quantidade_de_usos.data,
        )
        db.session.add(plano)
        db.session.commit()
        flash('Plano cadastrado com sucesso!', 'alert alert-success')
        return redirect(url_for('home.home'))
    return render_template('cadastro_plano.html', form_cadastro_plano=form_cadastro_plano)


@PLANO.route('/vincular_plano', methods=['GET', 'POST'])
def vincular_plano():
    planos = PlanoDeUso.buscar_todos_planos()
    planos_dict = [plano.to_dict() for plano in planos]
    clientes = Cliente.buscar_todos_clientes()
    clientes_dict = [cliente.to_dict() for cliente in clientes]
    if verificar_botao_apertado():
        cliente_id = request.form['cliente_id']
        plano_id = request.form['plano_id']
        if not verificar_cliente_existente(cliente_id, plano_id):
            return render_template('vincular_planos.html', planos=planos_dict, clientes=clientes_dict)
        cliente, plano = verificar_cliente_existente(cliente_id, plano_id)
        cliente.plano = plano
        cliente.saldo += plano.quantidade_de_usos
        db.session.commit()
        flash(f'O plano {plano.nome_do_plano} foi vinculado ao cliente {cliente.nome}', 'alert alert-success')
        return redirect(url_for('home.home'))
    return render_template('vincular_planos.html', planos=planos_dict, clientes=clientes_dict)


def verificar_cliente_existente(cliente_id, plano_id):
    cliente = Cliente.buscar_cliente_por_id(cliente_id)
    plano = PlanoDeUso.buscar_plano_por_id(plano_id)
    if cliente.plano and cliente.plano.nome_do_plano == plano.nome_do_plano:
        flash(f'O cliente {cliente.nome} já está vinculado ao plano {plano.nome_do_plano}', 'alert alert-warning')
        return None
    return cliente, plano


def verificar_botao_apertado():
    if 'vincular_plano_btn' in request.form:
        return True
    return False
