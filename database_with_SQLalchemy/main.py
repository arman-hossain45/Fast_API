from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from  typing import Annotated
import models
from database import engine,sessionlocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


# open the database

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()
@app.get('/')
def read_todos(db : Annotated[Session,Depends(get_db)]):
    db.query(Todos).all()
