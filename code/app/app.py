from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
class Names(Base):
    __tablename__ = "names"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(25))
    last_name = Column(String(25))
    age = Column(Integer())

engine = create_engine('sqlite:///:memory:')
metadata = MetaData()
Base.metadata.create_all(engine)  # Vytvoření tabulek
Session = sessionmaker(bind=engine)

fake_names = [
    Names(name="Elon", last_name="Muskrat", age=53),
    Names(name="Johnny", last_name="Depp", age=55),
    Names(name="Taylor", last_name="Drift", age=23),
    Names(name="Brad", last_name="Pitstop", age=33),
    Names(name="Angelina Joliet", last_name="Joliet", age=48),
    Names(name="Kim Carcrashian", last_name="Carcrashian", age=43),
    Names(name="Leonardo DiCapuccino", last_name="DiCapuccino", age=49),
    Names(name="Miley Virus", last_name="Virus", age=31),
    Names(name="Beyoncé Knows-all", last_name="Knows-all", age=42),
    Names(name="Dwayne 'The pebble' Johnson", last_name="Johnson", age=51),
]
session = Session()
session.add_all(fake_names)
session.commit()

class Name(BaseModel):
    first_name: str
    last_name: str | None = None
    age: float

app = FastAPI()

@app.get("/get_names/")
async def get_names(skip: int = 2, limit: int = 5):
    result = session.query(Names).limit(limit).offset(skip).all()
    return result


@app.post("/post_name")
async def post_name(post_name: str):
    result = session.add(Names(name=post_name))
    return {"message": "Item added successfully"}

@app.put("/put_name/")
async def put_name(name_id: int, name: str):
    session.query(Names).filter(Name.id == name_id).update({"name": name})
    return {"message": f"Name updated successfully to {name}"}

@app.delete("/del_name/")
async def dalete_item(name_id: int):
    session.query(Names).filter(Name.id == name_id).delete()
    return {"message": "Item deleted successfully"}

