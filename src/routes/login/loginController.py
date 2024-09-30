from routes.login import loginService
from routes.generalDto import Message
from utils.auth_bearer import JWTBearer
from fastapi import APIRouter, Depends, Response
from routes.login.loginDto import Login, Signup, Token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.get("/", dependencies=[Depends(JWTBearer())])
async def get_user(response: Response) -> Message:
    response.delete_cookie(key="Authorization:")
    return Message(message="DiniMueter")

@router.post("/login")
async def login(login: Login, response: Response) -> Message:
    token = loginService.getToken(login)
    response.set_cookie(
        key="Authorization:",
        value=f"Bearer {token}",
        httponly=True,
        # secure=True,
        samesite="lax"
    )
    return Message(message="Login successful")


@router.post("/signup")
async def login(signup: Signup) -> Token:
    return "You are logged in"

@router.post("/logout")
async def logout(response: Response) -> Message:
    response.delete_cookie(key="access_token")
    return Message(message="Successfully logged out")

