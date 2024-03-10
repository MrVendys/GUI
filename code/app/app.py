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
    fake_names_db.append(name)
    return {"message": "Name created successfully"}

@app.put("/pt_name/{name_id}")
async def update_item(name_id: int, name: Name):
    fake_names_db[name_id] = name
    return {"message": "Name updated successfully"}

@app.delete("/dl_name/{name_id}")
async def delete_item(name_id: int):
    fake_names_db.remove(fake_names_db[name_id])
    return {"message": "Name deleted successfully."}