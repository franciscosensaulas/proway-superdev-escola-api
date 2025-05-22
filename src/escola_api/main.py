from datetime import datetime

from fastapi import FastAPI

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
    ano_nascimento = datetime.now().year - idade # from datetime import datetime

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
