from src.banco_dados import conectar

from sqlalchemy.orm import Session

from src.database.models import Produto


def cadastrar(nome: str, id_categoria: int):
    conexao = conectar()
    cursor = conexao.cursor()
    sql = "INSERT INTO produtos (nome, id_categoria) VALUES (%s, %s)"
    dados = (nome, id_categoria)
    cursor.execute(sql, dados)
    conexao.commit()
    cursor.close()
    conexao.close()

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
    produtos = db.query(Produto).all()
    return produtos


def obter_por_id(id: int):
    conexao = conectar()
    cursor = conexao.cursor()
    sql = """select
        produtos.id,
        produtos.nome,
        categorias.id,
        categorias.nome
    from produtos
    inner join categorias on (produtos.id_categoria = categorias.id)
    where produtos.id = %s"""
    cursor.execute(sql, (id,))
    registro = cursor.fetchone()
    cursor.close()
    conexao.close()

    if registro is None:
        return None

    return {
        "id": registro[0],
        "nome": registro[1],
        "categoria": {
            "id": registro[2],
            "nome": registro[3]
        }
    }
