from typing import Union
from fastapi import FastAPI

from src.routes.login import loginController


app = FastAPI(title="eParts",
    description="""
Organize your electronic components and projects with ease. 🚀
""",
    version="0.0.1",
    contact={
        "name": "Lukas Zimmermann",
        "email": "lukas.zimmermann@schoggipopcorn.ch",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },)
app.include_router(loginController.router)
