from fastapi import APIRouter
from src.routes.login.loginDto import Login, Signup, Token, User

router = APIRouter(prefix="/user", tags=["User"])

@router.get("/")
async def get_user() -> User:
    return "Dini Mueter"

@router.post("/login")
async def login(login: Login) -> Token:
    return "You are logged in"


@router.post("/signup")
async def login(signup: Signup) -> Token:
    return "You are logged in"