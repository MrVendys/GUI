from fastapi import FastAPI
from sqlalchemy import Column, Integer, String, create_engine, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
class Name(Base):
    __tablename__ = "names"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(25))

engine = create_engine('sqlite:///:memory:')
metadata = MetaData()
Base.metadata.create_all(engine)  # Vytvoření tabulek
Session = sessionmaker(bind=engine)

fake_names = [
    Name(name="Elon Muskrat"),
    Name(name="Johnny Depp-ression"),
    Name(name="Taylor Drift"),
    Name(name="Brad Pitstop"),
    Name(name="Angelina Joliet"),
    Name(name="Kim Carcrashian"),
    Name(name="Leonardo DiCapuccino"),
    Name(name="Miley Virus"),
    Name(name="Beyoncé Knows-all"),
    Name(name="Dwayne 'The pebble' Johnson")
]
session = Session()
session.add_all(fake_names)
session.commit()

app = FastAPI()

@app.get("/get_name")
async def get_name():
    result = session.query(Name).all()
    return result


@app.post("/post_name")
async def post_name(post_name: str):
    result = session.add(Name(name=post_name))
    return {"message": "Item added successfully"}

@app.put("/put_name/")
async def put_name(name_id: int, name: str):
    session.query(Name).filter(Name.id == name_id).update({"name": name})
    return {"message": f"Name updated successfully to {name}"}

