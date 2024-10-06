from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from routes.login import loginController
from routes.product import productController
from utils.middleware import log_middleware
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI(title="eParts",
    description="Organize your electronic components and projects with ease. 🚀",
    version="0.0.1",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },)

app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)

app.include_router(loginController.router)
app.include_router(productController.router)
