import os
import jwt
import time
import json
from utils.logger import logger
from fastapi import Request, Response
from starlette.requests import Request as StarletteRequest

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"

async def __get_body(request: Request) -> str:
    if request.url.path.startswith("/auth"):
        return json.dumps({"message": "no body supported for /auth endpoints"})
    try:
        body = await request.json()
        body = json.dumps(body)
    except:
        try:
            body = await request.body()
            body = body.decode('utf-8')[:4096]
        except:
            pass

    return body if body else "-"

async def __get_user_from_token(request: Request) -> str:
    user = "Unknown"
    try:
        token = request.cookies.get("Authorization:")

        if token and token.startswith("Bearer "):
            token = token[len("Bearer "):]

        payload = jwt.decode(token.encode('utf-8'), SECRET_KEY.encode('utf-8'), algorithms=[ALGORITHM])
        user = payload.get("sub", "Unknown")
    except Exception as e:
        print(e)
    return user[0:255]

async def log_middleware(request: Request, call_next):
    start_time = time.time()

    body = await __get_body(request)

    async def receive_with_body():
        return {"type": "http.request", "body": body.encode("utf-8")}

    new_request = StarletteRequest(request.scope, receive=receive_with_body)
    response: Response = await call_next(new_request)

    user = await __get_user_from_token(new_request)

    log_dict = {
        'url': new_request.url.path,
        'method': new_request.method,
        'process_time': round(time.time() - start_time, 3),
        'response_code': response.status_code,
        'user': user,
        'body': body
    }

    if response.status_code < 400:
        logger.info(log_dict, extra=log_dict)
    else:
        logger.error(log_dict, extra=log_dict)

    return response
