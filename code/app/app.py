from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
    Names(name="Elon", last_name="Tusk", age=53),
    Names(name="Johnny", last_name="Depp-ression", age=55),
    Names(name="Taylor", last_name="Drift", age=23),
    Names(name="Brad", last_name="Pitstop", age=33),
    Names(name="Angelina", last_name="Joliet", age=48),
    Names(name="Kim", last_name="Carcrashian", age=43),
    Names(name="Leonardo", last_name="DiCapuccino", age=49),
    Names(name="Miley", last_name="Virus", age=31),
    Names(name="Beyoncé", last_name="Knows-all", age=42),
    Names(name="Dwayne 'The pebble'", last_name="Johnson", age=51),
]
session = Session()
session.add_all(fake_names)
session.commit()

class Name(BaseModel):
    first_name: str
    last_name: str | None = None
    age: float

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/gt_names/")
async def get_names(name: Names):
    return {"Number": name_id, "Name": name}