from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, length, ValidationError, NumberRange
from wtforms.widgets import TextInput
from desk_manager.models import Mesa

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
    ], render_kw={"placeholder": "Ex: 123.456.789-10"})
    telefone = StringField('', validators=[DataRequired(), length(min=2, max=40)],
                           render_kw={"placeholder": '(xx) xxxx-xxxx'})
    
    # imagem = FileField('', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
    botao_submit = SubmitField('Cadastrar Cliente')

class FormCadastroMesa(FlaskForm):
    numero = IntegerField('', widget=TextInput(), validators=[DataRequired(message="'Este campo deve conter apenas numeros'"), 
                                                              NumberRange(min=1, max=99999999)])
    
    botao_submit = SubmitField('Cadastrar Mesa')

    def validate_numero(self, field):
        mesa_existente = Mesa.query.filter_by(numero=field.data).first()
        if mesa_existente:
            raise ValidationError('Uma mesa com esse número já existe.')

class FormCadastroPlano(FlaskForm):
    nome_do_plano = StringField('', validators=[DataRequired()])
    quantidade_de_usos = IntegerField('', validators=[DataRequired()], render_kw={"placeholder": 'Ex: 5'})

    botao_submit = SubmitField('Cadastrar Plano')
