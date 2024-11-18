from desk_manager.models import Mesa, Reserva
from flask import Blueprint, render_template, request, redirect, url_for, flash
from desk_manager.extensions import db
from desk_manager.forms.cadastro import FormCadastroMesa
import uuid

MESA = Blueprint('mesa', __name__)

@MESA.route('/mesas')
def lista_mesas():
    mesas = Mesa.query.all()
    mesas_dict = [mesa.to_dict() for mesa in mesas]
    return render_template('lista_mesas.html', mesas=mesas_dict)

@MESA.route('/mesa/<string:mesa_id>/editar', methods=['GET'])
def editar_mesa(mesa_id):
    mesa = Mesa.query.get(mesa_id)
    return render_template('editar_mesa.html', mesa=mesa)

@MESA.route('/mesa/<string:mesa_id>/editar', methods=['POST'])
def atualizar_mesa(mesa_id):
    mesa = Mesa.query.get(mesa_id)
    mesa.numero = request.form['numero']
    db.session.commit()
    return redirect(url_for('mesa.lista_mesas'))

@MESA.route('/mesa/<string:mesa_id>/excluir', methods=['POST'])
def excluir_mesa(mesa_id):
    mesa = Mesa.query.get(mesa_id)

    for reserva in Reserva.query.all():
        if (reserva.mesa == mesa) and (reserva.estado == 1 or reserva.estado == 3):
            flash('Não é possível excluir mesas reservadas.', 'warning')
            return redirect(url_for('mesa.lista_mesas'))

    db.session.delete(mesa)
    db.session.commit()
    return redirect(url_for('mesa.lista_mesas'))
    

@MESA.route('/buscar_mesa/<string:numero>', methods=['GET'])
def buscar_mesa_por_numero(numero):
    mesa = Mesa.query.filter_by(numero=numero).first()
    if not mesa:
        return render_template('lista_mesas.html', mesa_escolhida=None)
    return render_template('lista_mesas.html', mesa_escolhida=mesa.to_dict())

@MESA.route('/cadastro_mesa', methods=['GET', 'POST'])
def cadastrar_mesa():
    form_cadastro_mesa = FormCadastroMesa()
    if form_cadastro_mesa.validate_on_submit():
        id = uuid.uuid4().hex[:8]

        numero = form_cadastro_mesa.numero.data
        mesa = Mesa.query.filter_by(numero=numero).first()
        if mesa:
            flash('Já existe uma mesa cadastrada com esse numero!', 'warning')
            return redirect(url_for('mesa.lista_mesas'))

        mesa = Mesa(
            id = id,
            numero = form_cadastro_mesa.numero.data,
        )
        db.session.add(mesa)
        db.session.commit()
        flash('Mesa cadastrada com sucesso!', 'alert alert-success')
        return redirect(url_for('home.home'))
    return render_template('cadastro_mesa.html', form_cadastro_mesa=form_cadastro_mesa)
