from . import db
from enum import Enum
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class TipoUsuario(Enum):
    COMPRADOR = 1
    VENDEDOR = 2

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    tipo_usuario = db.Column(db.Enum(TipoUsuario), nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)
    
    def __init__(self, nome, email, tipo_usuario, senha):
        self.nome = nome
        self.email = email
        self.tipo_usuario = tipo_usuario
        self.senha = generate_password_hash(senha)
    
    def verificar_senha(self, senha):
        return check_password_hash(self.senha, senha)
    
    def __repr__(self):
        return f'<Usuario {self.nome}>'

class Produto(db.Model):
    __tablename__ = 'produtos'
    
    produto_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, default=0)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('usuarios.user_id'))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    imagem = db.Column(db.String(100), nullable=False)
    
    vendedor = db.relationship('Usuario', backref=db.backref('produtos', lazy=True))
    
    def __repr__(self):
        return f'<Produto {self.nome}>'