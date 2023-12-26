from fastapi import FastAPI
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
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="templates"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

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

@app.get("/list", response_model=list[SCPCharacter])
async def list_characters(db: Session = Depends(get_db)):
    query = scp_table.select()
    return db.execute(query).fetchall()

@app.get("/character", response_model=SCPCharacter)
async def get_character(name: str, db: Session = Depends(get_db)):
    query = scp_table.select().where(scp_table.c.name == name)
    return db.execute(query).fetchone()

@app.post("/insert", response_model=SCPCharacter)
async def insert_character(character: SCPCharacter, db: Session = Depends(get_db)):
    db.execute(
        scp_table.insert().values(
            name=character.name, age=character.age, class_type=character.class_type
        )
    )
    db.commit()
    return character

@app.put("/update/{character_id}", response_model=SCPCharacter)
async def update_character(
    character_id: int, character: SCPCharacter, db: Session = Depends(get_db)
):
    db.execute(
        scp_table.update().where(scp_table.c.id == character_id).values(
            name=character.name, age=character.age, class_type=character.class_type
        )
    )
    db.commit()
    return character

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

"""
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
    Column("class_type", String),
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

templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/create", response_model=None)
async def create_character(character: SCPCharacter, db: Session = Depends(get_db)):
        db.execute(
            scp_table.insert().values(
                name=character.name, age=character.age, class_type=character.class_type
            )
        )
        db.commit()
        return {"message": "Character created successfully"}

@app.get("/list", response_model=list[SCPCharacter])
async def list_characters(db: Session = Depends(get_db)):
    query = scp_table.select()
    return db.execute(query).fetchall()

@app.get("/character", response_model=SCPCharacter)
async def get_character(name: str, db: Session = Depends(get_db)):
    query = scp_table.select().where(scp_table.c.name == name)
    return db.execute(query).fetchone()

@app.post("/insert", response_model=SCPCharacter)
async def insert_character(character: SCPCharacter, db: Session = Depends(get_db)):
    db.execute(
        scp_table.insert().values(
            name=character.name, age=character.age, class_type=character.class_type
        )
    )
    db.commit()
    return character

@app.put("/update/{character_id}", response_model=SCPCharacter)
async def update_character(
    character_id: int, character: SCPCharacter, db: Session = Depends(get_db)
):
    db.execute(
        scp_table.update().where(scp_table.c.id == character_id).values(
            name=character.name, age=character.age, class_type=character.class_type
        )
    )
    db.commit()
    return character

@app.delete("/delete/{character_id}")
async def delete_character(character_id: int, db: Session = Depends(get_db)):
    db.execute(scp_table.delete().where(scp_table.c.id == character_id))
    db.commit()
    return {"message": "Character deleted successfully"}

@app.post("/add")
async def add_character(
    name: str = Form(...),
    age: int = Form(...),
    class_type: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        db.execute(
            scp_table.insert().values(
                name=name, age=age, class_type=class_type
            )
        )
        db.commit()
        return {"message": "SCP adicionado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""