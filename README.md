
--- API - lugar para disponibilizar recursos/funcionalidades ---
https://realpython.com/fastapi-python-web-apis/

1. Objetivo - disponibilizar uma API para consulta de dados dos SCPs
(além de poder criar, editar e excluir)
2. URL base - localhost.com (local para onde estarei fazendo requisição - scpfoundation.com/api/...)
3. Endpoints:
   localhost/lista (GET) - (obter) todos os scps
   localhost/lista/id (GET) - um scp em específico
   localhost/lista (POST) - (criar) um scp
   localhost/lista/id (PUT) - modificar/(editar)
   localhost/lista/id (DELETE) - (deletar)
4. Recursos - SCPs
5. Ferramentas: FastAPI (estrutura web para criação de API), Uvicornb (servidor), python, JASON, HTML


1. config python (terminal) - criando um ambiente virtual
    clear
    cd + pasta
    pyenv local 3.12.0
    python -m venv env
    source env/bin/activate

2. instalação FastAPI e Uvicorn (pip):
    pip install uvicorn[standard]
    pip install fastapi[all]
    -> pip install fastapi uvicorn[standard]

3. criar primeira API:
    # main.py
    from fastapi import FastAPI
    app = FastAPI() --instância da classe FastAPI (principal ponto de interação)
    @app.get("/") --decorador c método get (mostra)
    async def root(): --detecta mudança em tempo real
    return {"message": "Hello World"} --dicionário

    - rodar (terminal):
    clear
    uvicorn main:app --reload  --atualização da var(add) no arquivo principal(main) no servidor(Uvi)
    -- clicar no link q aparecer (mostra uma mensagem JASON) --
    obs.: /docs no link mostra a documentação da api (por enquanto só tem uma rota, com get)

-- contextualização --
path: caminho após 1°/ - raiz
endpoint: rota (entre //)
operacional - método de requisição HTTP(comunica c os caminhos) - POST GET(busca) PUT(insere) DELETE OPTIONS HEAD PATCH TRACE

4. 



from fastapi import FastAPI, HTTPException
from models.personagens import Personagem
from pydantic import BaseModel
from typing import List
import uuid

app = FastAPI()


class PersonagemSchema(BaseModel):
    id: int
    nome: str
    altura: float
    peso: float
    habilidades: List[str]

personagens = []

@app.get("/personagens/", response_model=List[PersonagemSchema], summary="Obter lista de personagens")
def get_personagens():
    return [personagem.to_dict() for personagem in personagens]

@app.post("/personagens/", response_model=PersonagemSchema, summary="Criar um novo personagem")
def create_personagem(personagem: PersonagemSchema):
    personagem_id = str(uuid.uuid4())
    novo_personagem = Personagem(personagem_id, personagem.nome, personagem.altura, personagem.peso)#, personagem.habilidades)
    personagens.append(novo_personagem)
    return novo_personagem.to_dict()

@app.delete("/personagens/{personagem_id}", summary="Excluir um personagem")
def delete_personagem(personagem_id: str):
    for i, personagem in enumerate(personagens):
        if personagem.id == personagem_id:
            del personagens[i]
            return {"detail": "Personagem removido com sucesso"}
    raise HTTPException(status_code=404, detail="Personagem não encontrado")

@app.put("/personagens/{personagem_id}", response_model=PersonagemSchema, summary="Atualizar um personagem")
def update_personagem(personagem_id: str, updated_personagem: PersonagemSchema):
    """Atualiza um personagem existente."""
    for personagem in personagens:
        if personagem.id == personagem_id:
            personagem.nome = updated_personagem.nome
            personagem.altura = updated_personagem.altura
            personagem.peso = updated_personagem.peso
            personagem.habilidades = updated_personagem.habilidades
            return personagem.to_dict()
    raise HTTPException(status_code=404, detail="Personagem não encontrado")




<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SCP Characters API</title>
</head>
<body>
    <header>
        <!-- Seu cabeçalho aqui -->
    </header>
    <main>
        <!-- Conteúdo principal aqui -->
    </main>
    <h1>SCP Characters API</h1>
    <p>API for managing SCP characters</p>
    <footer>
        <p>API documentation: <a href="/docs">/docs</a></p>
    </footer>
</body>
</html>

-----------------

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker, Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi import Form
from fastapi import Depends
from pydantic import BaseModel

app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()

scp_table = Table(
    "scp_characters",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String, index=True),
    Column("age", Integer),
    Column("class", String),
)

metadata.create_all(bind=engine)

class SCPCharacter(BaseModel):
    name: str
    age: int
    class_type: str
    
characters = [
    {"id": 1, "name": "SCP-173", "age": 3, "class_type": "Euclid"},
    {"id": 2, "name": "SCP-096", "age": 14, "class_type": "Keter"},
    {"id": 3, "name": "SCP-682", "age": 320, "class_type": "Keter"},
]

"""
class SCPCharacter:
    def __init__(self, name: str, age: int, _class: str):
        self.name = name
        self.age = age
        self._class = _class
"""

templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""       
@app.post("/create", response_model=SCPCharacter)
async def create_character(character: SCPCharacter):
    new_id = len(characters) + 1
    new_character = {"id": new_id, **character.dict()}
    characters.append(new_character)
    return new_character

@app.post("/create", response_model=dict)
async def create_character(character: SCPCharacter):
    # Lógica para adicionar o personagem ao banco de dados ou outra ação necessária
    return {"message": "Personagem adicionado com sucesso!"}
"""

@app.post("/create", response_model=None)
async def create_character(character: SCPCharacter, db: Session = Depends(get_db)):
    db.execute(
        scp_table.insert().values(
            name=character.name, age=character.age, class_type=character.class_type
        )
    )
    db.commit()
    return character

@app.get("/read", response_model=list[SCPCharacter])
async def read_characters(db: Session = Depends(get_db)):
    query = scp_table.select()
    return db.execute(query).fetchall()

@app.delete("/delete/{character_id}")
async def delete_character(character_id: int, db: Session = Depends(get_db)):
    db.execute(scp_table.delete().where(scp_table.c.id == character_id))
    db.commit()
    return {"message": "Character deleted successfully"}

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/add")
async def add_character(
    name: str = Form(...),
    age: int = Form(...),
    class_type: str = Form(...),
    db: Session = Depends(get_db),
):
    db.execute(
        scp_table.insert().values(
            name=name, age=age, class_type=class_type
        )
    )
    db.commit()
    return RedirectResponse(url="/", status_code=303)

---------------

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SCP Foundation</title>
    <style>
        body {
            font-family: 'arial';
            background-color: #f0f0f0;
            color: #333;
            margin: 0;
        }
        h1 {
            font-family: 'serif';
            color: white;
            text-align: center;
        }

        header {
            background-color: #000;
            color: white;
            padding: 20px;
            text-align: center;
        }

        main {
            max-width: 500px;
            margin: 0 auto;
            padding: 20px;
        }

        form {
            background-color: #fff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }

        form label {
            display: block;
            margin-bottom: 10px;
        }

        form input {
            width: 100%;
            padding: 8px;
            margin-bottom: 16px;
            box-sizing: border-box;
        }

        form button {
            background-color: #000;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }

        h2 {
            color: #000;
            text-align: center;
        }

        footer {
            width: 100%;
            height: 600px;
            border: none;
            text-align: center;
        }

        #character-list {
            list-style-type: none;
            padding: 0;
            text-align: center;
        }

        #character-list li {
            margin-bottom: 10px;
            border: 1px solid #ccc;
            padding: 10px;
            width: 300px; /* Ajuste a largura conforme necessário */
        }
    </style>
</head>
<body>
    <header>
        <h1>SCP-Foundation creatures API</h1>
    </header>
    <main>
        <form id="character-form" onsubmit="addCharacte(event)"> /*action="/create" method="post"*/
            <label for="name">Name:</label>
            <input type="text" name="name" required><br>
            
            <label for="age">Age:</label>
            <input type="number" name="age" required><br>

            <label for="class_type">Class:</label>
            <input type="text" name="class_type" required><br>

            <button type="submit">Create SCP Character</button>
        </form>

        <h2>SCP Characters</h2>
            <ul id="character-list">
            </ul>

            <script>
                async function addCharacter(event) {
                    event.preventDefault();
            
                    const form = document.getElementById('character-form');
                    const formData = new FormData(form);
            
                    const response = await fetch('/create', {
                        method: 'POST',
                        body: formData,
                    });
            
                    if (response.ok) {
                        const result = await response.json();
                        // Adicione código para manipular a resposta JSON aqui
                        console.log(result.message);
            
                        // Limpe o formulário ou faça qualquer outra ação necessária
                        form.reset();
                    } else {
                        console.error('Erro ao adicionar personagem:', response.statusText);
                    }
                }

                const characters = [
                    { name: "SCP-173", age: 3, class_type: "Euclid" },
                    { name: "SCP-096", age: 14, class_type: "Keter" },
                    { name: "SCP-682", age: 320, class_type: "Keter" },
                ];
            
                // função para adicionar personagens à lista
                function populateCharacterList() {
                    const characterList = document.getElementById('character-list');
                    characters.forEach(character => {
                        const listItem = document.createElement('li');
                        listItem.innerHTML = `<strong>${character.name}</strong> - Age: ${character.age}, Class: ${character.class_type}`;
                        characterList.appendChild(listItem);
                    });
                }
                window.onload = populateCharacterList;
            </script>            
    </main>
    <footer>
        <p><a href="/docs" target="_blank"><h2>FastAPI Documentation</h2></a></p>
    </footer>
</body>
</html>
