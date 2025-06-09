from datetime import date

from fastapi import Depends
from sqlalchemy.orm import Session

from src.escola_api.app import router
from src.escola_api.database.modelos import MatriculaEntidade
from src.escola_api.dependencias import get_db
from src.escola_api.schemas.matricula_schemas import MatriculaCadastro, Matricula


@router.get("/api/matriculas", status_code=200, tags=["matriculas"])
def listar_todas_matriculas(db: Session = Depends(get_db)):
    matriculas = db.query(MatriculaEntidade).all()
    return matriculas

@router.post("/api/matriculas", status_code=200, tags=["matriculas"])
def cadastrar_matricula(form: MatriculaCadastro, db: Session = Depends(get_db)):
    matricula = MatriculaEntidade(
        aluno_id=form.aluno_id,
        curso_id=form.curso_id,
        data_matricula=date.today()
    )
    db.add(matricula)
    db.commit()
    db.refresh(matricula)
    return matricula


@router.delete("/api/matriculas/{id}", status_code=204, tags=["matriculas"])
def apagar_matricula():
    pass

@router.put("/api/matriculas/{id}", status_code=204, tags=["matriculas"])
def editar_matricula():
    pass

@router.get("/api/matriculas/{id}", status_code=204, tags=["matriculas"])
def obter_por_id_matricula():
    pass