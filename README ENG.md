# AsynchIO
## Installation instructions


# FastApi
## Installation instructions
```
```
Creating a virtual environment
```
python -m venv venv
```
Activate the virtual environment so that we can install all the libraries here
```
venv\scripts\activate
```

Installing the fastapi and uvicorn libraries
```
pip install fastapi uvicorn[standard]
```

Now we create a python file and import fastapi
```
from fastapi import FastAPI

app = FastAPI()
```
### Running the application
```
uvicorn {name of python file}:{name of FastAPI instance} --reload
```
In my case: 
```
uvicorn main:app --reload
```

## Programming
Once we have the working environment ready, it's time to program

### Endpoint GET

```
fake_names_db = [
    "Elon Muskrat",
    "Johnny Depp-ression",
    "Taylor Drift",
    "Brad Pitstop",
    "Angelina Joliet."
    "Kim Carcrashian."
    "Leonardo DiCapuccino."
    "Miley Virus."
    "Beyoncé Knows-all."
    "Dwayne 'The pebble' Johnson"
]

@app.get("/gt_names/")
async def get_names():
    return fake_names_db

```
FastAPI uses the so-called "Path and Querry parameters"

Path parameters: we work with the data we have in the URL
```
@app.get("/gt_name/{name_id}")
async def get_name(name_id: int):
    return fake_names_db[name_id]
```
Querry parameters: we work with the data that comes from the API in the so-called "body"
```
async def get_names(skip : int = 0, limit: int | None = None):
```

### Endpoint POST
```
@app.post("/cr_name/")
async def create_name(name: string):
    fake_names_db.append(name)

```
### Endpoint PUT
```
@app.put("/pt_name/{name_id}")
async def update_item(name_id: int):
    del fake_names_db[name_id]
    return {"message": "Item updated successfully"}
```
### Endpoint DELETE
```
@app.post("/dl_name/")
async def delete_item():
    return {"message": "POST new item"}
```

## pydantic
 Pydantic is a data validation library
 FastAPI is fully compatible with (and based on) the Pydantic library
 
 Why use it?
 Type Help
 Fast data validation
 JSON compatible
 Error messages

 Pydantic uses so-called BaseModels
```
from pydantic import BaseModel

class Name(BaseModel):
    name: str  
    people_with_name: PositiveInt | None = None
```
We're going to modify our code.

```
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, PositiveInt

app = FastAPI()

fake_names_db = [
    {"name": "Elon Tusk", "people_with_name": 3},
    {"name": "Johnny Depp-ression", "people_with_name": 2},
    { "name": "Taylor Drift", "people_with_name": 1},
    { "name": "Brad Pitstop", "people_with_name": 2},
    { "name": "Angelina Joliet", "people_with_name": 1},
    { "name": "Kim Carcrashian", "people_with_name": 2},
    { "name": "Leonardo DiCapuccino", "people_with_name": 3},
    { "name": "Oprah Windfury", "people_with_name": 0},
    { "name": "Ariana Grande Latte", "people_with_name": 2},
    { "name": "Dwayne Jonah Johnson", "people_with_name": 3}
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
    return {"message": "Name successfully removed."}
```
