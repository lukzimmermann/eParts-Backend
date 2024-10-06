from typing import Annotated
from routes.login import loginService
from routes.generalDto import Message
from routes.product.productDto import ProductDto
from utils.auth_bearer import JWTBearer
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from routes.product.productService import fetch_product_by_id, fetch_products

router = APIRouter(prefix="/product", tags=["Product"])

"""
Get all recorded products
"""
@router.get("/", dependencies=[Depends(JWTBearer())])
async def get_products(response: Response) -> list[ProductDto]:
    return fetch_products()

"""
Get product with specific id
"""
@router.get("/{product_id}", dependencies=[Depends(JWTBearer())])
async def get_product(product_id: Annotated[int, None], response: Response) -> ProductDto:
    return fetch_product_by_id(product_id)