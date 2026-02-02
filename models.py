from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    tipo = Column(String)  # Receita ou Despesa

class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True)
    descricao = Column(String)
    valor = Column(Float, nullable=False)
    data = Column(Date)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    categoria = relationship("Categoria")

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
