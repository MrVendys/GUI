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

@app.get("/gt_name/{name_id}")
async def get_name(name_id: int):
    return {"Number": name_id}