from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Temos uma classe chamada Categoria que herda as propriedades e métodos da Base
class Categoria(Base):
    # Nome da tabale no banco de dados
    __tablename__ = "categorias"

    # Coluna da PK id do tipo inteiro auto incrementável
    id = Column(Integer, primary_key=True, autoincrement=True)
    # Coluna do nome que n permite nulo
    nome = Column(String(255), nullable=False)
