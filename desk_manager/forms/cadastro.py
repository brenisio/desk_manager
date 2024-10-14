from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, DateTimeField, SelectField, HiddenField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, length, ValidationError
from datetime import datetime
from desk_manager.models import PeriodoReserva, Cliente


def validate_cpf(form, field):
    cpf = field.data
    if not cpf.isdigit():
        raise ValidationError('O CPF deve conter apenas números.')

    if len(cpf) != 11:
        raise ValidationError('O CPF deve ter exatamente 11 dígitos.')

    cliente_repetido = Cliente.query.filter_by(cpf=cpf).first()
    if cliente_repetido and cliente_repetido.id != form.id.data:
        raise ValidationError('CPF já cadastrado por outro cliente.')

def validate_telefone(form, field):
    telefone = field.data
    if not telefone.isdigit():
        raise ValidationError('O telefone deve conter apenas números.')
    if len(telefone) < 10:
        raise ValidationError('O telefone deve ter no mínimo 10 dígitos.')
    if len(telefone) > 11:
        raise ValidationError('O telefone deve ter no máximo 11 dígitos.')

class FormCadastroCliente(FlaskForm):
    id = HiddenField('ID')
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

class FormCadastroReserva(FlaskForm):
    data = StringField('', validators=[DataRequired()])
    def validate_data(self, field):
        try:
            # Tenta converter a string para um objeto datetime
            self.data.data = datetime.strptime(field.data, '%d/%m/%Y')
        except ValueError:
            raise ValidationError('Data inválida! Use o formato dd/mm/yyyy.')
        
    periodo = SelectField('', choices=[(periodo.value, periodo.name) for periodo in PeriodoReserva],
                           validators=[DataRequired()])
    cpf_cliente = StringField('', validators=[DataRequired()])
    numero_mesa = StringField('', validators=[DataRequired()])

    botao_submit = SubmitField('Cadastrar Reserva')