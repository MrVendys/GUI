from fastapi import FastAPI, HTTPException

app = FastAPI()

fake_names_db = [
    "Elon Tusk",
    "Johnny Depp-ression",
    "Taylor Drift",
    "Brad Pitstop",
    "Angelina Joliet",
    "Kim Carcrashian",
    "Leonardo DiCapuccino",
    "Oprah Windfury",
    "Ariana Grande Latte",
    "Dwayne John Jonah Johnson"
]

@app.get("/names/")
async def get_names():
    return fake_names_db

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id < 0 or item_id >= len(fake_names_db):
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_names_db[item_id]