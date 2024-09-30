from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class PriceDto(BaseModel):
    quantity: float
    price: float

class SupplierProductDto(BaseModel):
    number: str
    product_page: str
    price: Optional[list[PriceDto]] = None


class SupplierDto(BaseModel):
    id: int
    name: str
    product_detail: Optional[SupplierProductDto] = None

class ProductDto(BaseModel):
    id: int
    create_at: datetime
    update_at: datetime
    name: str
    category_id: int
    manufacture: str
    manufacture_number: str
    minimum_quantity: float
    suppliers: Optional[list[SupplierDto]] = None
