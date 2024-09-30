import csv
import time
import json

from sqlalchemy import Null
from models import Attribute, Category, Price, Product, ProductAttribute, ProductSupplier, Supplier, Unit
from utils.database import Database
from passlib.context import CryptContext
import numpy as np

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
session = Database().get_session()

def import_category() -> None:
    categories = _get_list_of_rows('src/csv/product_type.csv')
    for element in categories:
        category = Category(id=element[0], name=element[1])
        print(category)
        session.add(category)
    session.commit()

def import_products() -> None:
    products = _get_list_of_rows('src/csv/product.csv')
    for element in products:
        product = Product(
            id=element[0],
            name=element[1],
            category_id=element[2],
            manufacture_number=element[3],
            minimum_quantity=element[6],
            create_at=element[8],
            update_at=element[9],
            manufacture=element[11])
        print(product)
        session.add(product)
    session.commit()

def import_supplier() -> None:
    suppliers = _get_list_of_rows("src/csv/supplier.csv")
    for element in suppliers:
        supplier = Supplier(id=element[0], name=element[1])
        session.add(supplier)
    session.commit()

def import_product_supplier():
    product_suppliers = _get_list_of_rows("src/csv/product_supplier.csv")
    for element in product_suppliers:
        product_supplier = ProductSupplier(
            product_id = element[0],
            supplier_id = element[1],
            number = element[2],
            product_page = element[3]
        )
        print(product_supplier)
        session.add(product_supplier)
    session.commit()

def import_unit():
    units = _get_list_of_rows("src/csv/unit.csv")
    for element in units:
        unit = Unit(
            id = element[0],
            parent_id = element[2],
            name = element[1],
            factor = element[3]
        )
        print(unit)
        session.add(unit)
    session.commit()

def import_attribute():
    attributes = _get_list_of_rows("src/csv/valuename.csv")
    for element in attributes:
        attribute = Attribute(
            id = element[0],
            parent_id = None,
            unit_id = element[3],
            name = element[2]
        )
        print(attribute)
        session.add(attribute)
    session.commit()

def import_product_attribute():
    product_attributes = _get_list_of_rows("src/csv/product_value.csv")
    for element in product_attributes:
        product_attribute = ProductAttribute(
            product_id = element[0],
            unit_id = element[2],
            attribute_id = element[3],
            text_value = None,
            numeric_value = element[1]
        )
        print(product_attribute)
        session.add(product_attribute)
        session.commit()

def import_price():
    prices = _get_list_of_rows("src/csv/product_price.csv")
    for element in prices:
        price = Price(
            product_id = element[0],
            supplier_id = element[1],
            quantity = element[2],
            price = element[3]
        )
        print(price)
        session.add(price)
    session.commit()


def _get_list_of_rows(path: str) -> list[list[str]]:
    rows = []
    with open(path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            rows.append(row)
    return rows

def print_all_attributes(allData):
    start = time.time()
    allData = session.query(Product).all()
    print(f"{time.time()-start:.3f}s")

    for data in allData:
        print(data)
        for e in data.attributes:
            print(f"{e.attribute.name}: {e.numeric_value}{e.unit.name}")
        print()

def main():
    #import_category()
    #import_products()
    #import_supplier()
    #import_product_supplier()
    #import_unit()
    #import_attribute()
    #import_product_attribute()
    #import_price()

    product = session.query(Product).where(Product.id == 109).one_or_none()

    print(product.suppliers[0].supplier.product_suppliers)

if __name__ == "__main__":
    main()