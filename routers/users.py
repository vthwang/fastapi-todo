from fastapi import APIRouter, Depends, HTTPException
import models
from pydantic import BaseModel, Field
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
from .auth import get_current_user
from passlib.context import CryptContext
from models import User

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

models.Base.metadata.create_all(bind=engine)


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserVerification(BaseModel):
    password: str = Field(min_length=6)
    new_password: str = Field(min_length=6)


@router.get("/", status_code=status.HTTP_200_OK)
def read_user(user: user_dependency, db: db_dependency):
    return db.query(User).filter(User.id == user.get("id")).first()


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(
    user: user_dependency, db: db_dependency, user_verification: UserVerification
):
    user_model = db.query(User).filter(User.id == user.get("id")).first()
    if not bcrypt_context.verify(user_verification.password, user_model.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )
    user_model.password = bcrypt_context.hash(user_verification.new_password)
    db.commit()
    return {"message": "Password updated successfully"}
