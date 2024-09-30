from typing import Annotated
from routes.login import loginService
from routes.generalDto import Message
from routes.product.productDto import ProductDto
from utils.auth_bearer import JWTBearer
from fastapi import APIRouter, Depends, Query, Response
from routes.product.productService import get_product_from_db

router = APIRouter(prefix="/product", tags=["Product"])

@router.get("/", dependencies=[Depends(JWTBearer())])
async def get_product(product_id: Annotated[int, None], response: Response):
    return get_product_from_db(product_id)