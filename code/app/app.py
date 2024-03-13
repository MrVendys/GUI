from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, PositiveInt

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

app = FastAPI()
@app.get("/names")
async def get_name(bl: bool = False):
    if bl:
        return "Hodnota překonvertována na True"
    else:
        return "Hodnota překonvertována na False"