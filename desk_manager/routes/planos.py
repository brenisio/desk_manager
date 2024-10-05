from desk_manager.models import Plano
from flask import Blueprint, render_template, request, redirect, url_for, flash
from desk_manager.extensions import db
from desk_manager.forms.cadastro import FormCadastroMesa
import uuid


PLANO = Blueprint('plano', __name__)

@PLANO.route('/tipos_planos')
def lista_planos():
    planos = Plano.query.all()
    return render_template('lista_planos.html')
