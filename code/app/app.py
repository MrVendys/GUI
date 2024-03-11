from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, PositiveInt

class Name(BaseModel):
    name: str  
    people_with_name: PositiveInt | None = None

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, PositiveInt, EmailStr

app = FastAPI()

@app.get("/gt_name")
async def get_name():
    return {"Hello": "This is your get endpoint"}