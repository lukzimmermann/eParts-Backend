from typing import Annotated
from models import Attribute
from routes.login import loginService
from routes.generalDto import Message
from routes.product.productDto import ProductDto, AttributeDto, SimpleAttribute, UnitDto
from utils.auth_bearer import JWTBearer
from fastapi import APIRouter, Depends, Response
from routes.product.productService import fetch_product_by_id, fetch_products, fetch_attributes, fetch_units

router = APIRouter(prefix="/product", tags=["Product"])

"""
Get all attributes
"""
@router.get("/attributes/")  # Changed to /attributes
async def get_attributes() -> list[SimpleAttribute]:
    return fetch_attributes()

"""
Get all units
"""
@router.get("/units/")  # Changed to /attributes
async def get_units() -> list[UnitDto]:
    return fetch_units()


"""
Get all recorded products
"""
@router.get("/", dependencies=[Depends(JWTBearer())])
async def get_products(response: Response) -> list[ProductDto]:
    return fetch_products()

"""
Get product with specific id
"""
@router.get("/{product_id}/", dependencies=[Depends(JWTBearer())])
async def get_product(product_id: Annotated[int, None], response: Response) -> ProductDto:
    return fetch_product_by_id(product_id)


