from itertools import product
from fastapi import HTTPException
from sqlalchemy import func
from models import Attribute, Category, Price, Product, ProductAttribute, ProductDocument, ProductSupplier, Supplier, Transaction, Unit
from routes.product.productDto import AttributeDto, DocumentDto, PriceDto, ProductDto, SupplierDto, SupplierProductDto
from utils.database import Database

session = Database().get_session()

def fetch_products() -> Product:
    products = (
        session.query(
            Product,
            func.sum(Transaction.quantity).label('quantity')
        )
        .join(Transaction, Product.id == Transaction.product_id)
        .group_by(Product.id)
        .order_by(Product.id)
        .all()
    )

    return [
        ProductDto(
            id=product[0].id,
            create_at=product[0].create_at,
            update_at=product[0].update_at,
            name=product[0].name,
            category_id=product[0].category_id,
            category_name=__get_category_name(product[0].category_id),
            manufacture=product[0].manufacture,
            manufacture_number=product[0].manufacture_number,
            minimum_quantity=product[0].minimum_quantity,
            quantity=product[1]
        ) for product in products
    ]

def fetch_product_by_id(product_id) -> Product:
    product = session.query(Product).where(Product.id == product_id).one_or_none()
    if product == None:
        raise HTTPException(status_code=404, detail="Product not found")

    return ProductDto(
        id = product.id,
        create_at = product.create_at,
        update_at = product.update_at,
        name = product.name,
        category_id = product.category_id,
        category_name = __get_category_name(product.category_id),
        manufacture = product.manufacture,
        manufacture_number = product.manufacture_number,
        minimum_quantity = product.minimum_quantity,
        suppliers = __get_suppliers_of_product(product.id),
        attributes = __get_attribute_of_product(product.id),
        documents= __get_document(product_id)
        )

def __get_category_name(category_id: int):
    return session.query(Category).where(Category.id == category_id).one().name

def __get_suppliers_of_product(product_id):
    suppliers_response = session.query(ProductSupplier).where(ProductSupplier.product_id == product_id).all()
    suppliers: list[SupplierDto] = []
    for supplier in suppliers_response:
        supplier_details_response = session.query(Supplier).where(Supplier.id == supplier.supplier_id).one()
        price_response = session.query(Price).where(Price.product_id == product_id, Price.supplier_id == supplier.supplier_id).all()
        
        price_list: list[PriceDto] = []
        for p in price_response:
            price_list.append(PriceDto(quantity=p.quantity, price=p.price))

        supplier_product = SupplierProductDto(number=supplier.number, product_page=supplier.product_page, price=price_list)
        supplier = SupplierDto(id=supplier_details_response.id, name=supplier_details_response.name, product_detail=supplier_product)

        suppliers.append(supplier)
    
    return suppliers

def __get_attribute_of_product(product_id):
    attributes_response = (session.query(ProductAttribute, Attribute, Unit)
                           .join(Attribute, Attribute.id == ProductAttribute.attribute_id)
                           .join(Unit, Unit.id == ProductAttribute.unit_id)
                           .where(ProductAttribute.product_id == product_id)
                           .all())
    attributes: list[AttributeDto] = []


    for product_attribute, attribute, unit in attributes_response:
        attributes.append(AttributeDto(
            id = attribute.id,
            parent_id = attribute.parent_id,
            name = attribute.name,
            numeric_value = product_attribute.numeric_value,
            text_value = product_attribute.text_value,
            unit_id = unit.id,
            unit_name = unit.name
        ))

    return attributes

def __get_document(product_id):
    documents_response = session.query(ProductDocument).where(ProductDocument.product_id == product_id).all()

    documents: list[DocumentDto] = []

    for document in documents_response:
        documents.append(DocumentDto(
            description = document.description,
            type=document.file_name.split(".")[-1],
            url = f"http://127.0.0.1:8000/api/product/document/{document.id}"
        ))

    return documents