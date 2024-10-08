from flask import request, flash
from wtforms.validators import ValidationError
import re
from desk_manager.models import Mesa

class ValidaString():
    def __init__(self, mensagem=None):
        self.mensagem = mensagem or 'Este campo deve conter apenas letras e espaços'

    def __call__(self, dado):
        if not  re.match("^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", dado):
            flash(self.mensagem, 'warning')
            return False
        return True


class ValidaNumero():
    def __init__(self, mensagem=None):
        self.mensagem = mensagem or 'Este campo deve conter apenas numeros'

    def __call__(self, dado):
        if not str(dado).isdigit():
            flash(self.mensagem, 'warning')
            return False
        return True


def verifica_mesa_existente(numero, mesa_atual=None):
    mesa_existente = Mesa.query.filter_by(numero=numero).first()
    if mesa_existente and mesa_existente != mesa_atual:
        flash('Já existe uma mesa cadastrada com esse número!', 'warning')
        return False
    return True