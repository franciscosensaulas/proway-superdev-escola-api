from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from src.escola_api.app import router
from src.escola_api.database.banco_dados import SessionLocal
from src.escola_api.database.modelos import AlunoEntidade
from src.escola_api.schemas.aluno_schemas import Aluno, AlunoEditar, AlunoCadastro


# Função de dependência para obter uma sessão do banco de dados
def get_db():
    db = SessionLocal()  # Cria uma nova sessão do banco de dados
    try:
        yield db  # Retorna a sessão de forma que o FastAPI possa utilizá-la nas rotas
    finally:
        db.close()  # Garante que a sessão será fechada após o uso


@router.get("/api/alunos")
def listar_todos_alunos(db: Session = Depends(get_db)):
    alunos = db.query(AlunoEntidade).all()
    return alunos


@router.get("/api/alunos/{id}")
def obter_por_id_alunos(id: int, db: Session = Depends(get_db)):
    aluno = db.query(AlunoEntidade).filter(AlunoEntidade.id == id).first()
    if aluno:
        return Aluno(
            id=aluno.id,
            nome=aluno.nome,
            sobrenome=aluno.sobrenome,
            cpf=aluno.cpf,
            data_nascimento=aluno.data_nascimento,
        )
    # Lançando uma exceção com o status code de 404(não encontrado)
    raise HTTPException(status_code=404, detail=f"Aluno não encontrado com id: {id}")


@router.post("/api/alunos")
def cadastrar_aluno(form: AlunoCadastro, db: Session = Depends(get_db)):
    # instanciar um objeto da classe AlunoEntidade
    aluno = AlunoEntidade(
        nome=form.nome,
        sobrenome=form.sobrenome,
        cpf=form.cpf,
        data_nascimento=form.data_nascimento)

    db.add(aluno)
    db.commit()
    db.refresh(aluno)

    return aluno


@router.delete("/api/alunos/{id}", status_code=204)
def apagar_aluno(id: int, db: Session = Depends(get_db)):
    aluno = db.query(AlunoEntidade).filter(AlunoEntidade.id == id).first()
    if aluno:
        db.delete(aluno)
        db.commit()
        return
    raise HTTPException(status_code=404, detail=f"Aluno não encontrado com id: {id}")


@router.put("/api/alunos/{id}")
def editar_aluno(id: int, form: AlunoEditar, db: Session = Depends(get_db)):
    aluno = db.query(AlunoEntidade).filter(AlunoEntidade.id == id).first()
    if aluno:
        aluno.nome = form.nome
        aluno.sobrenome = form.sobrenome
        aluno.cpf = form.cpf
        aluno.data_nascimento = form.data_nascimento
        db.commit()
        db.refresh(aluno)
        return aluno
    raise HTTPException(status_code=404, detail=f"Aluno não encontrado com id: {id}")
