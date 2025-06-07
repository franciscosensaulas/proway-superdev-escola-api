from datetime import date

from pydantic import BaseModel, Field


class MatriculaBase(BaseModel):
    aluno_id: int = Field()
    curso_id: int = Field()


# listagem, obter por id (get)
class Matricula(MatriculaBase):
    data_matricula: date = Field(alias="dataMatricula")


# cadastro (post)
class MatriculaCadastro(MatriculaBase):
    pass


class MatriculaCadastro(BaseModel):
    curso_id: int = Field()
