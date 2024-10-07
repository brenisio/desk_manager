from desk_manager.models import Plano
from flask import Blueprint, render_template, request, redirect, url_for, flash
from desk_manager.extensions import db
from desk_manager.forms.cadastro import FormCadastroPlano
import uuid


PLANO = Blueprint('plano', __name__)

@PLANO.route('/tipos_planos')
def lista_planos():
    planos = Plano.query.all()
    planos_dict = [plano.to_dict() for plano in planos]
    return render_template('lista_planos.html', planos=planos_dict, plano_escolhido=None)


@PLANO.route('/plano/<string:plano_id>/editar', methods=['GET'])
def editar_plano(plano_id):
    plano = Plano.query.get(plano_id)
    return render_template('editar_planos.html', plano=plano)


@PLANO.route('/plano/<string:plano_id>/editar', methods=['POST'])
def atualizar_plano(plano_id):
    plano = Plano.query.get(plano_id)
    plano.nome_do_plano = request.form['nome_do_plano']
    plano.quantidade_de_usos = request.form['quantidade_de_usos']
    db.session.commit()
    return redirect(url_for('plano.lista_planos'))


@PLANO.route('/plano/<string:plano_id>/excluir', methods=['POST'])
def excluir_plano(plano_id):
    plano = Plano.query.get(plano_id)
    db.session.delete(plano)
    db.session.commit()
    return redirect(url_for('plano.lista_planos'))


@PLANO.route('/buscar_plano/<string:nome_do_plano>', methods=['GET'])
def buscar_plano_por_nome(nome_do_plano):
    plano = Plano.query.filter_by(nome_do_plano=nome_do_plano).first()
    if not plano:
        return render_template('lista_planos.html', plano_escolhido=None)
    plano_escolhido = plano.to_dict()
    return render_template('lista_planos.html', plano_escolhido=plano_escolhido)


@PLANO.route('/cadastro_plano', methods=['GET', 'POST'])
def cadastrar_plano():
    form_cadastro_plano = FormCadastroPlano()
    if form_cadastro_plano.validate_on_submit():
        id = uuid.uuid4().hex[:8]

        plano = Plano(
            id=id,
            nome_do_plano=form_cadastro_plano.nome_do_plano.data,
            quantidade_de_usos=form_cadastro_plano.quantidade_de_usos.data,
        )
        db.session.add(plano)
        db.session.commit()
        flash('Plano cadastrado com sucesso!', 'alert-success')
        return redirect(url_for('home.home'))
    return render_template('cadastro_plano.html', form_cadastro_plano=form_cadastro_plano)
