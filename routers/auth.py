from datetime import timedelta, datetime, timezone
from fastapi import APIRouter
from pydantic import BaseModel
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends
from models import User
from passlib.context import CryptContext
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import HTTPException
from jose import jwt

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

SECRET_KEY = "your-256-bit-secret-key"
ALGORITHM = "HS256"


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        return {"username": username, "id": user_id}
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(create_user_request: CreateUserRequest, db: db_dependency):
    user_model = User(
        username=create_user_request.username,
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        password=bcrypt_context.hash(create_user_request.password),
        role=create_user_request.role,
        is_active=True,
    )
    db.add(user_model)
    db.commit()


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    access_token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {"access_token": access_token, "token_type": "bearer"}
