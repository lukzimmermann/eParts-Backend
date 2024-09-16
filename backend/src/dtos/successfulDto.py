from pydantic import BaseModel


class Successful(BaseModel):
    response: str