from datetime import date
from sqlalchemy.orm import Session

from src.database.models import Cliente


def cadastrar(db: Session, nome: str, cpf: str, data_nascimento: date, limite: float):
    cliente = Cliente(
        nome=nome,
        cpf=cpf,
        data_nascimento=data_nascimento,
        limite=limite
    )
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


def obter_todos(db: Session):
    clientes = db.query(Cliente).all()
    return clientes


def obter_por_id(db: Session, id: int):
    cliente = db.query(Cliente).filter(Cliente.id == id).first()
    return cliente


def apagar(db: Session, id: int):
    cliente = db.query(Cliente).filter(Cliente.id == id).first()
    if not cliente:
        return 0 # Gambiarra
    db.delete(cliente)
    db.commit()
    return 1 # Gambiarra


def editar(db: Session, id: int, data_nascimento: date, limite: float):
    # Não permitiremos o usuário alterar o nome e cpf uma vez que foi cadastrado
    cliente = db.query(Cliente).filter(Cliente.id == id).first()
    if not cliente:
        return 0
    
    cliente.data_nascimento = data_nascimento
    cliente.limite = limite
    db.commit()
    return 1