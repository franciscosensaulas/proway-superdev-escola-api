from datetime import date

from pydantic import BaseModel, Field


class MatriculaBase(BaseModel):
    aluno_id: int = Field()
    curso_id: int = Field()


# listagem, obter por id (get)
class MatriculaAluno(BaseModel):
    nome: str = Field()
    sobrenome: str = Field()
    id: int = Field()

class Matricula(MatriculaBase):
    data_matricula: date = Field(alias="dataMatricula")
    aluno: MatriculaAluno = Field()
    id: int = Field()

    class Config:
        populate_by_name = True


# cadastro (post)
class MatriculaCadastro(MatriculaBase):
    pass


class MatriculaEditar(BaseModel):
    curso_id: int = Field()
