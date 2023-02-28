from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import List
import models
from sqlalchemy.orm import Session
from database import engine, SessionLocal


app = FastAPI()


class UserBase(BaseModel):
    email: str
    username: str
    hashed_password: str
    is_active: int


class ShowUsers(BaseModel):
    email: str
    username: str
    is_active: int

    class Config:
        orm_mode = True


context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return context.hash(password)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/users/show", response_model=List[ShowUsers])
async def show_all_users(db: Session = Depends(get_db)):
    result = db.query(models.Users).all()
    print(result)
    return [i for i in result]


@app.post("/user/create", status_code=201)
async def create_new_user(user: UserBase, db: Session = Depends(get_db)):
    user_model = models.Users()
    user_model.email = user.email
    user_model.username = user.username
    user_model.hashed_password = get_password_hash(user.hashed_password)
    user_model.is_active = user.is_active

    db.add(user_model)
    db.commit()

    return user_model
