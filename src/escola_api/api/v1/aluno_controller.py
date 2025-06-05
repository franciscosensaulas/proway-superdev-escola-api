from datetime import date

from fastapi import HTTPException

from src.escola_api.app import router
from src.escola_api.database.banco_dados import SessionLocal
from src.escola_api.database.modelos import Curso
from src.escola_api.schemas.aluno_schemas import Aluno, AlunoEditar, AlunoCadastro

alunos = [
    # instanciando um objeto da Class Aluno
    Aluno(id=1, nome="João", sobrenome="Diniz", cpf="062.950.959-55", dataNascimento=date(1990, 5, 25))
]

# Função de dependência para obter uma sessão do banco de dados
def get_db():
    db = SessionLocal()  # Cria uma nova sessão do banco de dados
    try:
        yield db  # Retorna a sessão de forma que o FastAPI possa utilizá-la nas rotas
    finally:
        db.close()  # Garante que a sessão será fechada após o uso


from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
@router.get("/api/alunos")
def listar_todos_alunos(db: Session = Depends(get_db)):
    alunos = db.query(Curso).all()
    return alunos


@router.get("/api/alunos/{id}")
def obter_por_id_alunos(id: int):
    for aluno in alunos:
        if aluno.id == id:
            return aluno

    # Lançando uma exceção com o status code de 404(não encontrado)
    raise HTTPException(status_code=404, detail=f"Aluno não encontrado com id: {id}")


@router.post("/api/alunos")
def cadastrar_aluno(form: AlunoCadastro):
    ultimo_id = max([aluno.id for aluno in alunos], default=0)

    # instanciar um objeto da classe Aluno
    aluno = Aluno(
        id=ultimo_id + 1,
        nome=form.nome,
        sobrenome=form.sobrenome,
        cpf=form.cpf,
        dataNascimento=form.data_nascimento)

    alunos.append(aluno)

    return aluno


@router.delete("/api/alunos/{id}", status_code=204)
def apagar_aluno(id: int):
    for aluno in alunos:
        if aluno.id == id:
            alunos.remove(aluno)
            return
    raise HTTPException(status_code=404, detail=f"Aluno não encontrado com id: {id}")


@router.put("/api/alunos/{id}")
def editar_aluno(id: int, form: AlunoEditar):
    for aluno in alunos:
        if aluno.id == id:
            aluno.nome = form.nome
            aluno.sobrenome = form.sobrenome
            aluno.cpf = form.cpf
            aluno.data_nascimento = form.data_nascimento
            return aluno
    raise HTTPException(status_code=404, detail=f"Aluno não encontrado com id: {id}")
