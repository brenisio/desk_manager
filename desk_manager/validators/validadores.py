from flask import request, flash
from wtforms.validators import ValidationError
import re

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
