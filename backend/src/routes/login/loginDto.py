
import datetime
from pydantic import BaseModel


class Login(BaseModel):
    username: str
    password: str

class Signup(BaseModel):
    username: str
    email:str
    password: str

class Token(BaseModel):
    token: str

class User(BaseModel):
    username: str
    create_at: datetime.datetime
    update_at: datetime.datetime
    disabled: bool