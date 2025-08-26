from sqlalchemy import (
    Column, String, Enum, Integer
)   
import enum
from . import db 

class TipoUsuario(enum.enum):
    VENDEDOR = "VENDEDOR"
    COMPRADOR = "COMPRADOR"

class Usuario(db.Model):
    __tablename__ = "Usuario"

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    tipo_usuario = Column(Enum(TipoUsuario,native_enum=True), nullable=False) 
