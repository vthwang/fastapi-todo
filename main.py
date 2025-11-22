from fastapi import FastAPI, Depends, HTTPException, Path
import models
from models import Todo
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/")
def read_all(db: db_dependency):
    return db.query(Todo).all()


@app.get("/todo/{todo_id}")
def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")
