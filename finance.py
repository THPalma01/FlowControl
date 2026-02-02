from datetime import date, datetime
import hashlib
from sqlalchemy import func

from database import Session
from models import Transacao, Categoria, Usuario

def faturamento_total():
    session = Session()
    total = session.query(func.sum(Transacao.valor))\
        .join(Categoria)\
        .filter(Categoria.tipo == "Receita")\
        .scalar()
    session.close()
    return total or 0

def total_despesas():
    session = Session()
    total = session.query(func.sum(Transacao.valor))\
        .join(Categoria)\
        .filter(Categoria.tipo == "Despesa")\
        .scalar()
    session.close()
    return total or 0

def lucro_liquido():
    return faturamento_total() - total_despesas()

def despesas_por_categoria():
    session = Session()
    dados = session.query(Categoria.nome, func.sum(Transacao.valor))\
        .join(Transacao)\
        .filter(Categoria.tipo == "Despesa")\
        .group_by(Categoria.nome)\
        .all()
    session.close()
    return dados

def faturamento_mensal():
    session = Session()
    dados = session.query(func.strftime("%Y-%m", Transacao.data),
                          func.sum(Transacao.valor))\
        .join(Categoria)\
        .filter(Categoria.tipo == "Receita")\
        .group_by(func.strftime("%Y-%m", Transacao.data))\
        .all()
    session.close()
    return dados

def ticket_medio():
    session = Session()
    media = session.query(func.avg(Transacao.valor))\
        .join(Categoria)\
        .filter(Categoria.tipo == "Receita")\
        .scalar()
    session.close()
    return media or 0

def listar_categorias():
    session = Session()
    categorias = session.query(Categoria).all()
    session.close()
    return categorias


def criar_categoria(nome, tipo):
    session = Session()
    nova = Categoria(nome=nome, tipo=tipo)
    session.add(nova)
    session.commit()
    session.close()


def adicionar_transacao(descricao, valor, data, categoria_id):
    session = Session()
    nova = Transacao(
        descricao=descricao,
        valor=valor,
        data=data,
        categoria_id=categoria_id
    )
    session.add(nova)
    session.commit()
    session.close()

def faturamento_periodo(data_inicio, data_fim):
    session = Session()
    total = session.query(func.sum(Transacao.valor))\
        .join(Categoria)\
        .filter(Categoria.tipo == "Receita")\
        .filter(Transacao.data.between(data_inicio, data_fim))\
        .scalar()
    session.close()
    return total or 0


def despesas_periodo(data_inicio, data_fim):
    session = Session()
    total = session.query(func.sum(Transacao.valor))\
        .join(Categoria)\
        .filter(Categoria.tipo == "Despesa")\
        .filter(Transacao.data.between(data_inicio, data_fim))\
        .scalar()
    session.close()
    return total or 0


def despesas_por_categoria_periodo(data_inicio, data_fim):
    session = Session()
    dados = session.query(Categoria.nome, func.sum(Transacao.valor))\
        .join(Transacao)\
        .filter(Categoria.tipo == "Despesa")\
        .filter(Transacao.data.between(data_inicio, data_fim))\
        .group_by(Categoria.nome)\
        .all()
    session.close()
    return dados


def faturamento_mensal_periodo(data_inicio, data_fim):
    session = Session()
    dados = session.query(func.strftime("%Y-%m", Transacao.data),
                          func.sum(Transacao.valor))\
        .join(Categoria)\
        .filter(Categoria.tipo == "Receita")\
        .filter(Transacao.data.between(data_inicio, data_fim))\
        .group_by(func.strftime("%Y-%m", Transacao.data))\
        .all()
    session.close()
    return dados

def listar_transacoes_periodo(data_inicio, data_fim):
    session = Session()
    dados = session.query(
        Transacao.descricao,
        Transacao.valor,
        Transacao.data,
        Categoria.nome,
        Categoria.tipo
    )\
    .join(Categoria)\
    .filter(Transacao.data.between(data_inicio, data_fim))\
    .order_by(Transacao.data.desc())\
    .all()

    session.close()
    return dados

def resumo_periodo(data_inicio, data_fim):
    receitas = faturamento_periodo(data_inicio, data_fim)
    despesas = despesas_periodo(data_inicio, data_fim)
    lucro = receitas - despesas
    return receitas, despesas, lucro


def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()


def criar_usuario(nome, email, senha):
    session = Session()
    try:
        usuario = Usuario(
            nome=nome,
            email=email,
            senha=hash_senha(senha)
        )
        session.add(usuario)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def autenticar_usuario(email, senha):
    session = Session()
    senha_hash = hash_senha(senha)
    user = session.query(Usuario)\
        .filter_by(email=email, senha=senha_hash)\
        .first()
    session.close()
    return user