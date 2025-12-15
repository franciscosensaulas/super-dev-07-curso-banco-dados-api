from src.banco_dados import conectar
from sqlalchemy.orm import Session

from src.database.models import Categoria


def cadastrar(db: Session, nome: str):
    categoria = Categoria(nome=nome)
    db.add(categoria) # INSERT INTO categorias (nome) VALUES (%s)
    db.commit() # Concretização do insert no banco
    db.refresh(categoria) # Atribuir para a categoria o id que foi gerado no db
    return categoria


def editar(id: int, nome: str):
    conexao = conectar()

    cursor = conexao.cursor()
    
    sql = "UPDATE categorias SET nome = %s WHERE id = %s"
    dados = (nome, id)
    cursor.execute(sql, dados)
    
    conexao.commit()

    linhas_afetadas = cursor.rowcount

    cursor.close()

    conexao.close()
    return linhas_afetadas


def apagar(id: int) -> int:
    conexao = conectar()
    cursor = conexao.cursor()
    sql = "DELETE FROM categorias WHERE id = %s"
    dados = (id,)
    cursor.execute(sql, dados)
    conexao.commit()

    linhas_afetadas = cursor.rowcount

    cursor.close()
    conexao.close()
    return linhas_afetadas

def obter_todos():
    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute("SELECT id, nome  FROM categorias")

    registros = cursor.fetchall()

    cursor.close()
    conexao.close()
    categorias = []

    for registro in registros:
        categoria = {
            "id": registro[0],
            "nome": registro[1]
        }
        categorias.append(categoria)

    return categorias


def obter_por_id(id: int):
    conexao = conectar()
    cursor = conexao.cursor()
    sql = "SELECT id, nome FROM categorias WHERE id = %s"
    dados = (id,)
    cursor.execute(sql, dados)

    registro = cursor.fetchone()
    if not registro:
        return None

    return {
        "id": registro[0],
        "nome": registro[1]
    }
