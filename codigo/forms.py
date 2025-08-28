from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from .models import Usuario, TipoUsuario
from werkzeug.security import check_password_hash,generate_password_hash

class RegistrationForm(FlaskForm):
    nome = StringField('Nome completo', validators=[
        DataRequired(message='Campo obrigatório'),
        Length(min=2, max=100, message='O nome deve ter entre 2 e 100 caracteres')
    ], render_kw={"placeholder": "Digite seu nome completo"})
    
    email = StringField('E-mail', validators=[
        DataRequired(message='Campo obrigatório'),
        Email(message='Digite um e-mail válido') 
    ], render_kw={"placeholder": "Digite seu e-mail"})
    
    tipo_usuario = SelectField('Tipo de conta', 
                              choices=[(tipo.value, tipo.name.capitalize()) for tipo in TipoUsuario],
                              validators=[DataRequired(message='Selecione um tipo de conta')])
    
    senha = PasswordField('Senha', validators=[
        DataRequired(message='Campo obrigatório'),
        Length(min=6, message='A senha deve ter pelo menos 6 caracteres')
    ], render_kw={"placeholder": "Crie uma senha"})
    
    confirmar_senha = PasswordField('Confirmar senha', validators=[
        DataRequired(message='Campo obrigatório'),
        EqualTo('senha', message='As senhas não coincidem')
    ], render_kw={"placeholder": "Digite a senha novamente"})
    
    submit = SubmitField('Criar conta')
    
    def validate_nome(self, field):
        if Usuario.query.filter_by(nome=field.data).first():
            raise ValidationError('Este nome de usuário já está em uso')
    
    def validate_email(self, field):
        if Usuario.query.filter_by(email=field.data).first():
            raise ValidationError('Este e-mail já está cadastrado')

class LoginForm(FlaskForm):
    nome = StringField('Nome de usuário', validators=[
        DataRequired(message='Campo obrigatório')
    ], render_kw={"placeholder": "Digite seu nome de usuário"})
    
    senha = PasswordField('Senha', validators=[
        DataRequired(message='Campo obrigatório')
    ], render_kw={"placeholder": "Digite sua senha"})
    
    submit = SubmitField('Entrar')
    
    def validate_nome(self, field):
        user = Usuario.query.filter_by(nome=field.data).first()
        if user is None:
            raise ValidationError('Usuário não encontrado')
    
    def validate_senha(self, field):
        user = Usuario.query.filter_by(nome=self.nome.data).first()

        if user and not check_password_hash(user.senha, field.data):
            raise ValidationError('Senha incorreta')
        
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length
from .models import Produto

class AddProductForm(FlaskForm):
    nome = StringField('Nome do Produto', validators=[
        DataRequired(message='Campo obrigatório'),
        Length(min=2, max=100, message='O nome deve ter entre 2 e 100 caracteres')
    ], render_kw={"placeholder": "Digite o nome do produto"})
    
    descricao = TextAreaField('Descrição', validators=[
        DataRequired(message='Campo obrigatório'),
        Length(min=10, max=500, message='A descrição deve ter entre 10 e 500 caracteres')
    ], render_kw={"placeholder": "Descreva o produto", "rows": 4})
    
    preco = DecimalField('Preço (R$)', validators=[
        DataRequired(message='Campo obrigatório'),
        NumberRange(min=0.01, message='O preço deve ser maior que zero')
    ], render_kw={"placeholder": "0,00", "step": "0.01"})
    
    estoque = IntegerField('Estoque', validators=[
        DataRequired(message='Campo obrigatório'),
        NumberRange(min=1, message='O estoque deve ser pelo menos 1')
    ], render_kw={"placeholder": "Quantidade disponível"})
    
    imagem = FileField('Imagem do Produto', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Apenas imagens são permitidas')
    ])
    
    submit = SubmitField('Adicionar Produto')
    
    def validate_nome(self, field):
        if Produto.query.filter_by(nome=field.data).first():
            raise ValidationError('Já existe um produto com este nome')