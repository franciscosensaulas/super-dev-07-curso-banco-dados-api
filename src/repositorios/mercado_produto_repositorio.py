from src.banco_dados import conectar

from sqlalchemy.orm import Session, contains_eager

from src.database.models import Produto


def cadastrar(db: Session, nome: str, id_categoria: int):
    produto = Produto(nome=nome, id_categoria=id_categoria)
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto

def editar(id: int, nome: str, id_categoria: int):
    conexao = conectar()
    cursor = conexao.cursor()
    sql = "UPDATE produtos SET nome = %s, id_categoria = %s WHERE id = %s"
    dados = (nome, id_categoria, id)
    cursor.execute(sql, dados)
    conexao.commit()
    linhas_afetadas = cursor.rowcount
    cursor.close()
    conexao.close()
    return linhas_afetadas


def apagar(id: int):
    conexao = conectar()
    cursor = conexao.cursor()
    sql = "DELETE FROM produtos WHERE id = %s"
    dados = (id,)
    cursor.execute(sql, dados)
    conexao.commit()
    linhas_afetadas = cursor.rowcount
    cursor.close()
    conexao.close()
    return linhas_afetadas


def obter_todos(db: Session):
    produtos = db.query(Produto).options(contains_eager(Produto.categoria)).all()
    return produtos


def obter_por_id(db: Session, id: int):
    produto = db.query(Produto)\
        .options(contains_eager(Produto.categoria))\
        .filter(Produto.id == id)\
        .first()

    return produto
