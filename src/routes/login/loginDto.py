from pydantic import BaseModel


class LoginDto(BaseModel):
    email: str
    password: str

class SignupDto(BaseModel):
    first_name: str
    last_name: str
    email:str
    job_title: str
    password: str

class TokenDto(BaseModel):
    access_token: str

class OrganisationDto(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True 

class UserDto(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    job_title: str
    organisations: list[OrganisationDto]
    
    class Config:
        from_attributes = True 
