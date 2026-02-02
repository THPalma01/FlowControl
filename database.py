from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

engine = create_engine("sqlite:///smartfinance.db")
Session = sessionmaker(bind=engine)

def criar_banco():
    Base.metadata.create_all(engine)