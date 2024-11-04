import os
from typing import Annotated
from routes.login import loginService
from routes.generalDto import Message
from routes.product.productDto import ProductDto, AttributeDto, SimpleAttribute, UnitDto
from utils.auth_bearer import JWTBearer
from fastapi import APIRouter, Depends, Response
from fastapi.responses import FileResponse, StreamingResponse
from routes.product.productService import fetch_product_by_id, fetch_products, fetch_attributes, fetch_units
from minio import Minio

router = APIRouter(prefix="/product", tags=["Product"])

MINIO_BUCKET = str(os.getenv('MINIO_BUCKET'))

client = Minio( str(os.getenv('MINIO_HOST')),
    access_key = str(os.getenv('MINIO_ACCESS_KEY')),
    secret_key = str(os.getenv('MINIO_SECRET_KEY')),
    secure = False,
)


BUCKET = "eparts"

@router.get("/download/{file_name}")
async def download_file(file_name: str):
    objects = client.get_object(BUCKET, file_name)

    return StreamingResponse(objects.stream(32*1024), media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={file_name}"})

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


