from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, DateTimeField, SelectField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, length, ValidationError
from datetime import datetime
from desk_manager.models import PeriodoReserva

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