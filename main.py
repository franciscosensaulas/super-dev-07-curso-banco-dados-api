from fastapi import Depends, FastAPI, HTTPException

from classes import AlunoCalcularMedia, CategoriaCriar, CategoriaEditar, ClienteCriar, ClienteEditar, ProdutoCriar, ProdutoEditar
from src.database.conexao import get_db
from src.repositorios import mercado_categoria_repositorio, mercado_cliente_repositorio, mercado_produto_repositorio

from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

app = FastAPI()
# pip install pymysql
# pip freeze > requirements.txt



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/greetings")
def saudacoes():
    return {"mensagem":  "Hello World"}


# /calculadora?numero1=9&numero2=1
@app.get("/calculadora")
def calculadora(numero1: int, numero2: int):
    soma = numero1 + numero2
    return {"resultado": soma}


# (query) vai depois da ? ex.: /calculadora/expert?operacao=soma&n1=100&n2=200
@app.get("/calculadora/expert")
def calculadora_expert(operacao: str, n1: int, n2: int):
    if operacao not in ["somar", "subtrair"]:
        raise HTTPException(
            status_code=400,
            detail="Operação inválida. Opções disponíveis [somar/subtrair]"
        )

    if operacao == "somar":
        resultado = n1 + n2
        return {
            "n1": n1,
            "n2": n2,
            "operacao": operacao,
            "resultado": resultado,
        }
    elif operacao == "subtrair":
        resultado = n1 - n2
        return {
            "n1": n1,
            "n2": n2,
            "operacao": operacao,
            "resultado": resultado,
        }


@app.post("/aluno/calcular-media")
def calcular_media(aluno_dados: AlunoCalcularMedia):
    nota1 = aluno_dados.nota1
    nota2 = aluno_dados.nota2
    nota3 = aluno_dados.nota3
    media = (nota1 + nota2 + nota3) / 3
    return {
        "media": media,
        "nome_completo": aluno_dados.nome_completo
    }


@app.get("/api/v1/categorias", tags=["Categorias"])
def listar_categorias(db: Session = Depends(get_db)):
    categorias = mercado_categoria_repositorio.obter_todos(db)
    return categorias


# /api/v1/categorias
# Método POST
# Body: {"nome": "Batatinha"}
@app.post("/api/v1/categorias", tags=["Categorias"])
def cadastrar_categoria(categoria: CategoriaCriar, db: Session = Depends(get_db)):
    mercado_categoria_repositorio.cadastrar(db, categoria.nome)
    return {
        "status": "ok"
    }

# /api/v1/categorias/10
# Método DELETE
@app.delete("/api/v1/categorias/{id}", tags=["Categorias"])
def apagar_categoria(id: int, db: Session = Depends(get_db)):
    linhas_afetadas = mercado_categoria_repositorio.apagar(db, id)
    
    if linhas_afetadas == 1:
        return {
            "status": "ok"
        }
    else:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
# /api/v1/categorias/10
# Método PUT
# Body {"nome": "Batatona 2.0"}
@app.put("/api/v1/categorias/{id}", tags=["Categorias"])
def alterar_categoria(id: int, categoria: CategoriaEditar, db: Session = Depends(get_db)):
    linhas_afetadas = mercado_categoria_repositorio.editar(db, id, categoria.nome)
    if linhas_afetadas == 1:
        return {
            "status": "ok"
        }
    else:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    

    
@app.get("/api/v1/categorias/{id}", tags=["Categorias"])
def buscar_categoria_por_id(id: int, db: Session = Depends(get_db)):
    categoria = mercado_categoria_repositorio.obter_por_id(db, id)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return categoria


@app.get("/api/v1/produtos", tags=["Produtos"])
def listar_todos_produtos(db: Session = Depends(get_db)):
    produtos = mercado_produto_repositorio.obter_todos(db)
    return produtos


# cadastrar
@app.post("/api/v1/produtos", tags=["Produtos"])
def cadastrar_produto(produto: ProdutoCriar):
    mercado_produto_repositorio.cadastrar(produto.nome, produto.id_categoria)
    return {"status": "ok"}


# editar
@app.put("/api/v1/produtos/{id}", tags=["Produtos"])
def alterar_produto(id: int, produto: ProdutoEditar):
    linhas_afetadas = mercado_produto_repositorio.editar(id, produto.nome, produto.id_categoria)
    if linhas_afetadas != 1:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    return {"status": "ok"}


# apagar
@app.delete("/api/v1/produtos/{id}", tags=["Produtos"])
def apagar_produto(id: int):
    linhas_afetadas = mercado_produto_repositorio.apagar(id)
    if linhas_afetadas != 1:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    return {"status": "ok"}

# obter por id
@app.get("/api/v1/produtos/{id}", tags=["Produtos"])
def obter_produto_por_id(id: int):
    produto = mercado_produto_repositorio.obter_por_id(id)
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    return produto


@app.post("/api/v1/clientes", tags=["Clientes"])
def cadastrar_cliente(cliente: ClienteCriar, db: Session = Depends(get_db)):
    cliente = mercado_cliente_repositorio.cadastrar(
        db, 
        cliente.nome, 
        cliente.cpf,
        cliente.data_nascimento,
        cliente.limite
    )
    return cliente


@app.get("/api/v1/clientes", tags=["Clientes"])
def listar_clientes(db: Session = Depends(get_db)):
    clientes = mercado_cliente_repositorio.obter_todos(db)
    return clientes


@app.delete("/api/v1/clientes/{id}", tags=["Clientes"])
def apagar_cliente(id: int, db: Session = Depends(get_db)):
    linhas_afetadas = mercado_cliente_repositorio.apagar(db, id)
    if not linhas_afetadas:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return {"status": "ok"}


@app.put("/api/v1/clientes/{id}", tags=["Clientes"])
def editar_cliente(id: int, cliente: ClienteEditar, db: Session = Depends(get_db)):
    linhas_afetadas = mercado_cliente_repositorio.editar(
        db, id, cliente.data_nascimento, cliente.limite,
    )
    if not linhas_afetadas:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return {"status": "ok"}


@app.get("/api/v1/clientes/{id}", tags=["Clientes"])
def listar_cliente(id: int, db: Session = Depends(get_db)):
    cliente = mercado_cliente_repositorio.obter_por_id(db, id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

# Ex.1 Criar um endpoint do tipo POST /aluno/calcular-frequencia
# Criar uma classe AlunoFrequencia
#   nome
#   quantidade_letivos
#   quantidade_presencas
# Payload:
#   nome do aluno
#   quantidade letivos
#   quantidade presencas
#   
#   qtd letivos     100
#   qtd presencas   
#   (qtd presencas * 100) / qtd letivos



# Criar um endpoint 'pessoa/nome-completo' para concatenar o nome da pessoa
#   Receber dois query params: nome e sobrenome
#   Retornar no seguinte formato {"nomeCompleto": "John Doe"}
# Criar um endpoint 'pessoa/calcular-ano-nascimento' para calcular o ano de nascimento
#   Query param: idade
#   Calcular o ano de nascimento
#   Retornar {"anoNascimento": 1991}
# Criar um endpoint 'pessoa/imc' para calcular o imc da pessoa
#   Query param: altura, peso
#   Calcular o imc
#   Retornar {"imc": 20.29}
# Alterar o endpoint 'pessoa/imc' para retornar o status do imc
#   Descobrir o status do IMC
#   Retornar {"imc"': 20.29, "Obesidade III"}
# fastapi dev main.py
# 127.0.0.1:8000/docs
# 127.0.0.1:8000/greetings

# ------------------------------------------------------------
# Passos para criar um novo endpoint
# Criar a tabela no SQL => CREATE TABLE ....
# Adicionar a classe no src/database/models.py
# Criar o repositório src/repositorios/mercado_<nome>_repositorio.py
#   Criar a função cadastrar
# Criar a classe <Nome>Criar e <Nome>Editar no arquivo classes.py
# Adicionar rota(endpoint) no main.py de cadastro
#   @app.post......

