from dataclasses import dataclass, field
from datetime import datetime

import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.openapi.models import Response
from fastapi.openapi.utils import status_code_ranges

app = FastAPI()


@app.get("/")
def index():
    return {"mensagem": "Olá mundo"}


@app.get("/calculadora")
def calculadora(numero1: int, numero2: int):
    soma = numero1 + numero2
    return {"soma": soma}


# http://127.0.0.1:8000/processar-cliente?nome=Pedro&sobrenome=Pascal&idade=27
@app.get("/processar-cliente")
def processar_dados_cliente(nome: str, idade: int, sobrenome: str):
    # nome_completo => snake_case
    # NomeCompleto => PascalCase
    # nomeCompleto => camelCase
    # nome-completo => kebab-case
    nome_completo = nome + " " + sobrenome
    ano_nascimento = datetime.now().year - idade  # from datetime import datetime

    if ano_nascimento >= 1990 and ano_nascimento < 2000:
        decada = "decada de 90"
    elif ano_nascimento >= 1980 and ano_nascimento < 1990:
        decada = "decada de 80"
    elif ano_nascimento >= 1970 and ano_nascimento < 1980:
        decada = "decada de 70"
    else:
        decada = "decada abaixo de 70 ou acima de 90"

    return {
        "nome_completo": nome_completo,
        "ano_nascimento": ano_nascimento,
        "decada": decada,
    }


# class CursoTradicional:
#     def __init__(self, id: int, nome: str, sigla: str):
#         self.id = id
#         self.nome = nome
#         self.sigla = sigla
# from dataclasses import dataclass, field
@dataclass
class Curso:
    id: int = field()
    nome: str = field()
    sigla: str = field()


@dataclass
class CursoCadastro:
    nome: str = field()
    sigla: str = field()


@dataclass
class CursoEditar:
    nome: str = field()
    sigla: str = field()


cursos = [
    # instanciando um objeto da classe Curso
    Curso(id=1, nome="Python Web", sigla="PY1"),
    Curso(id=2, nome="Git e GitHub", sigla="GT")
]


# localhost:8000/docs
@app.get("/api/cursos")
def listar_todos_cursos():
    return cursos


@app.get("/api/cursos/{id}")
def obter_por_id_curso(id: int):
    for curso in cursos:
        if curso.id == id:
            return curso

    # Lançando uma exceção com o status code de 404(não encontrado)
    raise HTTPException(status_code=404, detail=f"Curso não encontrado com id: {id}")


# CRUD
# C => create   => Método post
# R => read     => Métod get
# U => update   => Método put
# D => delete   => Método delete

@app.post("/api/cursos")
def cadastrar_curso(form: CursoCadastro):
    ultimo_id = max([curso.id for curso in cursos], default=0)

    # instanciar um objeto da classe Curso
    curso = Curso(id=ultimo_id + 1, nome=form.nome, sigla=form.sigla)

    cursos.append(curso)

    return curso


@app.delete("/api/cursos/{id}", status_code=204)
def apagar_curso(id: int):
    for curso in cursos:
        if curso.id == id:
            cursos.remove(curso)
            return
    raise HTTPException(status_code=404, detail=f"Curso não encontrado com id: {id}")


@app.put("/api/cursos/{id}", status_code=200)
def editar_curso(id: int, form: CursoEditar):
    for curso in cursos:
        if curso.id == id:
            curso.nome = form.nome
            curso.sigla = form.sigla
            return curso
    raise HTTPException(status_code=404, detail=f"Curso não encontrado com id: {id}")


if __name__ == "__main__":
    uvicorn.run("main:app")
