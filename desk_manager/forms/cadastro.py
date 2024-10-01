from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, length, ValidationError

def validate_cpf(form, field):
    cpf = field.data
    if not cpf.isdigit():
        raise ValidationError('O CPF deve conter apenas números.')
    if len(cpf) != 11:
        raise ValidationError('O CPF deve ter exatamente 11 dígitos.')

class FormCadastroCliente(FlaskForm):
    nome = StringField('', validators=[DataRequired()])
    cpf = StringField('CPF', validators=[
        DataRequired(),
        length(min=11, max=11, message="O CPF deve ter exatamente 11 dígitos."),
        validate_cpf
    ])
    telefone = StringField('', validators=[DataRequired(), length(min=2, max=40)])
    
    # imagem = FileField('', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
    botao_submit = SubmitField('Cadastrar Cliente')

