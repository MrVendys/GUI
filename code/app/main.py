from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Create SQLite database engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a SQLAlchemy session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define a SQLAlchemy model
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

# Create tables in the database
Base.metadata.create_all(bind=engine)

# Define Pydantic models for request and response data
class ItemCreate(BaseModel):
    name: str
    description: str

class ItemOut(BaseModel):
    id: int
    name: str
    description: str

# Create FastAPI app instance
app = FastAPI()

templates = Jinja2Templates(directory="app/templates")
# Endpoint to create a new item
@app.post("/items/put/", response_model=ItemOut)
def create_item(item: ItemCreate):
    db = SessionLocal()
    db_item = Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Endpoint to get an item by ID
@app.get("/items/{item_id}", response_model=ItemOut)
def read_item(item_id: int):
    db = SessionLocal()
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.get("/items/get/", response_model=list[ItemOut])
def read_items(request: Request):
    db = SessionLocal()
    items = db.query(Item).all()
    return templates.TemplateResponse("index.html", {"request": request, "items":items})

# Endpoint to update an item by ID
@app.put("/items/put/", response_model=ItemOut)
def update_item(item_id: int, item: ItemCreate):
    db = SessionLocal()
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.name = item.name
    db_item.description = item.description
    db.commit()
    db.refresh(db_item)
    return db_item

# Endpoint to delete an item by ID
@app.delete("/items/{item_id}", response_model=dict)
def delete_item(item_id: int):
    db = SessionLocal()
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully"}

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
