from email.policy import default

from database.db import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key= True)
    nome = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    nomeUsuario= db.Column(db.String(20), unique=True, nullable=False)
    tipo = db.Column(db.Enum('admin', 'comum'), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefone = db.Column(db.String(15))

class Product(db.Model):
    __tablename__ = 'produto'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False )
    descricao = db.Column(db.Text)
    categoria = db.Column(db.String(15))
    preco = db.Column(db.Integer(), nullable=False)
    validade = db.Column(db.Date)
    quantidade = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(10), default='und', nullable=False)
    disponibilidade = db.Column(db.Boolean, default= True, nullable=False)

class Comment(db.Model):
    __tablename__ = 'comentario'

    id = db.Column(db.Integer, primary_key=True)
    comentario = db.Column(db.Text, nullable=False)
    produto = db.Column(db.Integer, db.ForeignKey('Product.id'), nullable = False)
    usuario = db.Column(db.Integer, db.ForeignKey('User.id'), nullable = False)
    dataHora = db.Column(db.DateTime, default=db.func.current_timestamp())
