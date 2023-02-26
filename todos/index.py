from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field

import models
from database import engine, SessionLocal


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Todo(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=-1, lt=11, description="priority between 0 and 10")
    completed: int = Field(gt=-1, lt=2, description="completed between 0 and 1")


def raise_exception(name):
    return HTTPException(status_code=404, detail=f"{name} not found")


class CompleteEnum(str, Enum):
    FALSE = "0"
    TRUE = "1"


@app.get("/")
async def get_all(
    db: Session = Depends(get_db), completed: Optional[CompleteEnum] = None
):
    """
    Return all todo's
    """
    result = db.query(models.Todo).all()

    if completed:
        result = (
            db.query(models.Todo).filter(models.Todo.completed == completed.value).all()
        )

    return result


@app.get("/todo/{id_}")
async def get_current_todo(id_: int, db: Session = Depends(get_db)):
    """
    Return todo by his id
    """
    temporary = db.query(models.Todo).filter(models.Todo.id == id_).first()
    if not temporary is None:
        return temporary
    raise raise_exception(id_)


@app.post("/", status_code=201)
async def create_new_todo(todo: Todo, db: Session = Depends(get_db)):
    """
    Add new todo
    """
    todo_model = models.Todo()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.completed = todo.completed
    todo_model.priority = todo.priority

    db.add(todo_model)
    db.commit()
    return {"status": "Successfully"}


@app.put("/todo/{id_}", status_code=200)
async def change_todo(id_: int, todo: Todo, db: Session = Depends(get_db)):
    """
    Update todo
    """
    temporary = db.query(models.Todo).filter(models.Todo.id == id_).first()
    if temporary:
        temporary.title = todo.title
        temporary.description = todo.description
        temporary.completed = todo.completed
        temporary.priority = todo.priority

        db.add(temporary)
        db.commit()
        return {"status": "Success change"}

    raise raise_exception(id_)


@app.delete("/todo/{id_}", status_code=204)
async def delete_todo(id_: int, db: Session = Depends(get_db)):
    """
    Delete todo
    """
    temporary = db.query(models.Todo).filter(models.Todo.id == id_)
    if temporary.first():
        temporary.delete()
        db.commit()
        return {"status": "Success"}
    raise raise_exception(id_)
