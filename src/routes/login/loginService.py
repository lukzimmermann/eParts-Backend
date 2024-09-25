import os
import jwt
from models import User
from typing import Annotated
from dotenv import load_dotenv
from utils.database import Database
from routes.login.loginDto import Token, Login
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = Database().get_session()

def getToken(form_data: Login) -> Token:
    user = __authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = __create_access_token(
        data={"sub": user.name},
        expires_delta=access_token_expires,
    )
    return access_token

def __authenticate_user(username: str, password: str):
    user = db.query(User).filter(User.name == username).first()
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