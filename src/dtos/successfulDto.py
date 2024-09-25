from pydantic import BaseModel

class LoginData(BaseModel):
    username: str
    password: str

class Successful(BaseModel):
    response: str