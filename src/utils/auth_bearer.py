import os
import jwt
from dotenv import load_dotenv
from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        token = request.cookies.get("Authorization:")

        #if token is None:
        #    raise HTTPException(status_code=403, detail="No authorization token provided.")
        #if token.startswith("Bearer "):
        #    token = token[len("Bearer "):]
#
        #if not self.verify_jwt(token):
        #    raise HTTPException(status_code=403, detail="Invalid token or expired token.")
        return token

    def verify_jwt(self, token: str) -> bool:
        is_token_valid: bool = False
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        if payload:
            is_token_valid = True

        return is_token_valid