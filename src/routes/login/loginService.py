import os
import jwt
from sqlalchemy import JSON
from models import User
from dotenv import load_dotenv
from utils.database import Database
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, Request
from datetime import datetime, timedelta, timezone
from routes.login.loginDto import TokenDto, LoginDto, UserDto, OrganisationDto

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = Database().get_session()


def get_token(form_data: LoginDto):
    user = __authenticate_user(form_data.email, form_data.password)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    user_dto = __transform_to_UserDto(user)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = __create_access_token(
        data={"id": user.id, 
              "mail": user.email, 
              "organisation": [org.model_dump() for org in user_dto.organisations]},
        expires_delta=access_token_expires,
    )

    return {"token": access_token, "user": user_dto}

   
def get_user_from_token(request: Request):
    payload = __get_payload_from_token(request)
    user = db.query(User).where(User.email==payload["mail"]).first()
    return __transform_to_UserDto(user)

def __transform_to_UserDto(user: User) -> UserDto:
    organisations = [
        OrganisationDto(id=org.organisation.id, name=org.organisation.name)
        for org in user.organisations
    ]

    return UserDto(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        job_title=user.job_title,
        organisations=organisations
    )

def __authenticate_user(email: str, password: str):
    user = db.query(User).where(User.email==email).first()
    if not user:
        return False
    if not __verify_password(password, user.password_hash):
        return False
    return user

def __create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def __verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def __get_payload_from_token(request: Request):
    token = request.cookies.get("Authorization:")
    if token.startswith("Bearer "):
        token = token[len("Bearer "):]

    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])