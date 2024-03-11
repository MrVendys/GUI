# AsynchIO
## Návod na instalaci


# FastApi :runner:
## Návod na instalaci

:one: Vytvoření virtuálního prostředí
```
python -m venv venv
```

:two: Aktivace virtuálního prostředí, aby se nám všechny knihovny instalovali sem
```
venv\scripts\activate
```

:three: Nainstalování knihoven fastapi a uvicorn
```
pip install fastapi uvicorn[standard]
```

:four: Vytvoření python souboru a naimportování FastAPI
```
from fastapi import FastAPI

app = FastAPI()
```

### Spouštění aplikace
```
uvicorn {jmeno python souboru}:{jmeno FastAPI instance} --reload
```
V mém případě: 
```
uvicorn main:app --reload
```

## Programování :computer:
Jakmile máme připravené pracovní prostředí, je čas programovat

Podíváme se na 4 základní endpointy
### Endpoint GET
Základní syntax endpointů
```
@app.get("/gt_name")
async def get_name():
    return {"Hello": "This is your get endpoint"}
```

FastAPI používá tzv "Path and Querry parametrs"

1. Path parametrs: pracujeme s daty, které jsou součástí URL adresy.  
```
@app.get("/gt_name/{name}")
async def get_name(name):
    return {"Hello": name}
```

Teď, když si to vyzkoušíme, tak náš výstup by mohl vypadat takto:

![alt text](code/app/img/get_pepa.png)

Ale i takto

![alt text](code/app/img/get_5.png)

Nebo takto

![alt text](code/app/img/get_ujep.png)

Neřekli jsme FastAPI, jaký datový typ požadujeme, tak to všechno konvertuje na typ string.  
Kdybychom chtěli zadávat jenom hodnoty typu int, tak než to dělat přes složitou podmínku ve funkci, tak využijeme funkci FastAPI,
která to dělá sama

```
@app.get("/gt_name/{name_id}")
async def get_name(name_id: int):
    return {"Number": name_id}
```
Následný output je už int:  
![alt text](code/app/img/get_int.png)

Jinak bychom dostali tuto krásnou chybovou hlášku od knihovny pydantic, o které se dozvíme zachvíli.
```
{"detail":[{"type":"int_parsing","loc":["path","name"],  
"msg":"Input should be a valid integer,  
unable to parse string as an integer","input":"pepa","url":"https://errors.pydantic.dev/2.6/v/int_parsing"}]}
```
> [!TIP]<details>
<summary> ÚKOL </summary>
Pod tento endpoint si zkopírujte tento:  

```python
@app.get("/gt_name/5")
async def get_name():
    return {"Number": "Vymysli si něco"}
```

Jaký return to vrátí?
</details>


2. Querry parametrs: Pracujeme s daty, které nám přijdou z tzv "body"
```
async def get_names(skip : int = 0, limit: int = 10):
```

Samozřejmě můžeme kombinovat Path a Querry parametrs nebo jich napsat několik
```
@app.put("/names/{name_id}")
async def update_name(name_id: int, name: str, user: User):
```
### Endpoint POST
Skrz body nám přijde string 'name' a ten přidáme do db

Nad náš get endpoint si přidáme falešnou db, kterou budme testovat naše endpointy:
```
fake_names_db = [
    "Elon Muskrat",
    "Johnny Depp-ression",
    "Taylor Drift",
    "Brad Pitstop",
    "Angelina Joliet",
    "Kim Carcrashian",
    "Leonardo DiCapuccino",
    "Miley Virus",
    "Beyoncé Knows-all",
    "Dwayne 'The pebble' Johnson"
]
```

Nyní k post
```
@app.post("/cr_name/")
async def create_name(name: string):
    fake_names_db.append(name)
    return {"message": "Item added successfully"}
```
### Endpoint PUT
Skrz body nám přijde int 'name_id' a string 'name'. Podle intu přepíšeme požadovaný text v db
```
@app.put("/pt_name/{name_id}")
async def update_item(name_id: int, name: str):
    fake_names_db[name_id] = name
    return {"message": "Item updated successfully"}
```
### Endpoint DELETE
Skrz body nám přijde int 'name_id'. Podle intu odstraníme požadovaný text v db
```
@app.put("/pt_name/{name_id}")
async def update_item(name_id: int):
    del fake_names_db[name_id]
    return {"message": "Item deleted successfully"}
```

## Pydantic
 Pydantic je knihovna na validaci dat  
 FastAPI je plně kompatibilní (a založena na) knihovně Pydantic
 
### Proč ho používat?

 Nápověda pro typy 
 Rychlá validace dat  
 Kompatibilní s JSON  
 Chybové hlášky  

 Pydantic používá tzv. BaseModely
 BaseModel -> třída, podle které fastapi (pydantic) ověřuje, že data přišla celá a ve správných typech. (Nenapsali jsme "text" do typu int)
           -> nahrazuje query parametrs za třídu
```
from pydantic import BaseModel, PositiveInt

class Name(BaseModel):
    name: str  
    people_with_name: PositiveInt | None = None
```

Přepíšeme náš kód, aby využíval BaseModely

```
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, PositiveInt

app = FastAPI()

fake_names_db = [
    {"name": "Elon Tusk", "people_with_name": 3},
    {"name": "Johnny Depp-ression", "people_with_name": 2},
    {"name": "Taylor Drift", "people_with_name": 1},
    {"name": "Brad Pitstop", "people_with_name": 2},
    {"name": "Angelina Joliet", "people_with_name": 1},
    {"name": "Kim Carcrashian", "people_with_name": 2},
    {"name": "Leonardo DiCapuccino", "people_with_name": 3},
    {"name": "Oprah Windfury", "people_with_name": 0},
    {"name": "Ariana Grande Latte", "people_with_name": 2},
    {"name": "Dwayne John Jonah Johnson", "people_with_name": 3}
]

class Name(BaseModel):
    name: str  
    people_with_name: PositiveInt | None = None

@app.get("/names/")
async def get_names():
    return fake_names_db

@app.get("/name/{name_id}")
async def get_item(name_id: int):
    return fake_names_db[name_id]

@app.post("/cr_name/")
async def create_name(name: Name):
    fake_names_db.append(name.model_dump(dict))
    return {"message": "Name created successfully"}

@app.put("/pt_name/{name_id}")
async def update_item(name_id: int, name: Name):
    fake_names_db[name_id] = name.model_dump(dict)
    return {"message": "Name updated successfully"}

@app.delete("/dl_name/{name_id}")
async def delete_item(name_id: int):
    fake_names_db.remove(fake_names_db[name_id])
    return {"message": "Name deleted successfully."}
```

## Připojení na databázi

### Instalace
```
pip install sqlalchemy
```

Naimportování potřebných knihoven

```
from sqlalchemy import Column, Integer, String, DateTime, Enum, MetaData, func, create_engine, inspect
from sqlalchemy.orm import relationship, declarative_base
```

Vytvoření tabulky

```
Base = declarative_base()

class NameTable(Base):
	__tablename__ = 'nameTable'
	id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(25))
```
