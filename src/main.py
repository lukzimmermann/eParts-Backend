from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from routes.login import loginController
from routes.product import productController
from utils.middleware import log_middleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="eParts",
    description="Organize your electronic components and projects with ease. 🚀",
    version="0.0.1",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },)

origins = [
    "http://localhost:3000",  # React App in development
    "http://localhost:5173",  # Vite-based React app in development
    "https://yourfrontend.com",  # Your production frontend
    "http://10.0.0.193:5173",
    "*"
]

# Add CORS middleware to allow requests from specified origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specific domains
    allow_credentials=True,  # Allows cookies or authorization headers
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers (including custom headers)
)

app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)

app.include_router(loginController.router)
app.include_router(productController.router)
