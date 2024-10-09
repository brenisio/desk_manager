from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, length, ValidationError

def validate_cpf(form, field):
    cpf = field.data
    if not cpf.isdigit():
        raise ValidationError('O CPF deve conter apenas números.')
    if len(cpf) != 11:
        raise ValidationError('O CPF deve ter exatamente 11 dígitos.')

def validate_telefone(form, field):
    telefone = field.data
    if not telefone.isdigit():
        raise ValidationError('O telefone deve conter apenas números.')
    if len(telefone) < 10:
        raise ValidationError('O telefone deve ter no mínimo 10 dígitos.')
    if len(telefone) > 11:
        raise ValidationError('O telefone deve ter no máximo 11 dígitos.')

class FormCadastroCliente(FlaskForm):
    nome = StringField('', validators=[DataRequired()])
    cpf = StringField('CPF', validators=[
        DataRequired(),
        length(min=11, max=11, message="O CPF deve ter exatamente 11 dígitos."),
        validate_cpf
    ], render_kw={"placeholder": "Ex: 12345678910"})
    telefone = StringField('', validators=[
        DataRequired(),
        length(min=10, max=11, message="O telefone deve ter entre 10 e 11 dígitos."),
        validate_telefone
    ],render_kw={"placeholder": '(xx) xxxx-xxxx'})
    
    botao_submit = SubmitField('Cadastrar Cliente')

class FormCadastroMesa(FlaskForm):
    numero = StringField('', validators=[DataRequired(), length(min=1, max=40)])
    
    botao_submit = SubmitField('Cadastrar Mesa')

class FormCadastroPlano(FlaskForm):
    nome_do_plano = StringField('', validators=[DataRequired()])
    quantidade_de_usos = IntegerField('', validators=[DataRequired()], render_kw={"placeholder": 'Ex: 5'})

    botao_submit = SubmitField('Cadastrar Plano')
