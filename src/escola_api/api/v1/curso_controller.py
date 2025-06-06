from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from src.escola_api.app import router
from src.escola_api.database.banco_dados import SessionLocal
from src.escola_api.database.modelos import CursoEntidade
from src.escola_api.schemas.curso_schemas import CursoEditar, CursoCadastro


# Função de dependência para obter uma sessão do banco de dados
def get_db():
    db = SessionLocal()  # Cria uma nova sessão do banco de dados
    try:
        yield db  # Retorna a sessão de forma que o FastAPI possa utilizá-la nas rotas
    finally:
        db.close()  # Garante que a sessão será fechada após o uso


@router.get("/api/cursos")
def listar_todos_cursos(db: Session = Depends(get_db)):
    cursos = db.query(CursoEntidade).all()
    return cursos


# CRUD
# C => create   => Método post
# R => read     => Métod get
# U => update   => Método put
# D => delete   => Método delete

@router.post("/api/cursos")
def cadastrar_curso(form: CursoCadastro, db: Session = Depends(get_db)):
    # instanciar um objeto da classe Curso
    curso = CursoEntidade(nome=form.nome, sigla=form.sigla)
    db.add(curso)  # INSERT
    db.commit()  # Efetivando o registro na tabela
    db.refresh(curso)  # preenchendo o id que foi gerado no banco de dados

    return curso


@router.delete("/api/cursos/{id}", status_code=204)
def apagar_curso(id: int, db: Session = Depends(get_db)):
    curso = db.query(CursoEntidade).filter(CursoEntidade.id == id).first()
    if curso:
        db.delete(curso)
        db.commit()
        return
    raise HTTPException(status_code=404, detail=f"Curso não encontrado com id: {id}")


@router.put("/api/cursos/{id}", status_code=200)
def editar_curso(id: int, form: CursoEditar, db: Session = Depends(get_db)):
    curso = db.query(CursoEntidade).filter(CursoEntidade.id == id).first()
    if curso:
        curso.nome = form.nome
        curso.sigla = form.sigla
        db.commit()
        db.refresh(curso)
        return curso
    raise HTTPException(status_code=404, detail=f"Curso não encontrado com id: {id}")


@router.get("/api/cursos/{id}")
def obter_por_id_curso(id: int, db: Session = Depends(get_db)):
    curso = db.query(CursoEntidade).filter(CursoEntidade.id == id).first()
    if curso:
        return curso

    # Lançando uma exceção com o status code de 404(não encontrado)
    raise HTTPException(status_code=404, detail=f"Curso não encontrado com id: {id}")
