from sqlalchemy import Column, Date, Double, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Temos uma classe chamada Categoria que herda as propriedades e métodos da Base
class Categoria(Base):
    # Nome da tabale no banco de dados
    __tablename__ = "categorias"

    # Coluna da PK id do tipo inteiro auto incrementável
    id = Column(Integer, primary_key=True, autoincrement=True)
    # Coluna do nome que n permite nulo
    nome = Column(String(255), nullable=False)

    produtos = relationship("Produto", back_populates="categoria")


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    cpf = Column(String(14), nullable=False)
    data_nascimento = Column(Date, nullable=True)
    limite = Column(Double, nullable=True)

    # nullable=False campo é obrigatório
    # nullable=True campo ñ é obrigatório


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)

    # FK que relaciona a PK (categorias.id)
    id_categoria = Column(Integer, ForeignKey("categorias.id"))

    categoria = relationship("Categoria", back_populates="produtos")
