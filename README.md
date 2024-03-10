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

@app.get("/gt_names/")
async def get_names():
    return fake_names_db

```
FastAPI používá tzv "Path and Querry parametrs"

1. Path parametrs: pracujeme s daty, které jsou součástí URL adresy. 
    Buď s nimi můžeme dál pracovat:
```
@app.get("/gt_name/**{name_id}**")
async def get_name(name_id: int):
    return {"Number": name_id}
```
    Nebo je můžeme staticky deklarovat (podmínka)
```
@app.get("/gt_name/**5**)
async def get_name(name_id: int):
    return {"Number": name_id}
```

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
```
@app.post("/cr_name/")
async def create_name(name: string):
    fake_names_db.append(name)
    return {"message": "Item added successfully"}
```
### Endpoint PUT
```
@app.put("/pt_name/{name_id}")
async def update_item(name_id: int, name: str):
    fake_names_db[name_id] = name
    return {"message": "Item updated successfully"}
```
### Endpoint DELETE
```
@app.put("/pt_name/{name_id}")
async def update_item(name_id: int):
    del fake_names_db[name_id]
    return {"message": "Item deleted successfully"}
```

## pydantic
 Pydantic je knihovna na validaci dat  
 FastAPI je plně kompatibilní (a založena na) knihovně Pydantic
 
 Proč ho používat?

 Nápověda typů
 Rychlá validace dat
 Kompatibilní s JSON
 Chybové hlášky

 Pydantic používá tzv BaseModely
```
from pydantic import BaseModel

class Name(BaseModel):
    name: str  
    people_with_name: PositiveInt | None = None
```
Půjdeme upravit náš kód.

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
    if name_id < 0 or name_id >= len(fake_names_db):
        raise HTTPException(status_code=404, detail="Name not found")
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
