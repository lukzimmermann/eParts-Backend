import os
import csv
import time
import json
import uuid
from pathlib import Path

from sqlalchemy import Null
from models import Attribute, Category, DocumentCategory, Organisation, Price, Product, ProductAttribute, ProductDocument, ProductSupplier, Supplier, Transaction, Unit, User, UserOrganisation
from utils.database import Database
from passlib.context import CryptContext
from minio import Minio

MINIO_BUCKET = str(os.getenv('MINIO_BUCKET'))

client = Minio( str(os.getenv('MINIO_HOST')),
    access_key = str(os.getenv('MINIO_ACCESS_KEY')),
    secret_key = str(os.getenv('MINIO_SECRET_KEY')),
    secure = False,
)
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
            unit_base_id = element[3],
            name = element[2],
            is_title = False,
            is_numeric = True
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
            numeric_value = element[1],
            position = 1
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

def import_document():
    session.add(DocumentCategory(name = "Datasheet"))
    session.add(DocumentCategory(name = "Pinout"))
    session.commit()

    documents = _get_list_of_rows("src/csv/product_document.csv")
    for element in documents:
        file_type = element[4].split(".")[-1].lower()
        new_file_name = f'{uuid.uuid4()}.{file_type}'
        category_id = ""
        if element[2] == "Datasheet": category_id = 1
        if element[2] == "Pinout": category_id = 2

        file = Path('/Users/lukas/Desktop/DataSheets/' + element[4])

        with file.open("rb") as file_data:
            result = client.put_object(
                MINIO_BUCKET, new_file_name, file_data,
                length=-1,
                part_size=10*1024*1024,
            )
            print(
                "created {0} object; etag: {1}, version-id: {2}".format(
                    result.object_name, result.etag, result.version_id,
                ),
        )
    
        document = ProductDocument(
             id = element[0],
             product_id = element[1],
             category_id = category_id,
             description = "",
             file_name = new_file_name
        )
        print(document)
        session.add(document)
    session.commit()

def import_transaction():
    products = _get_list_of_rows('src/csv/product.csv')
    for element in products:
        transaction = Transaction(
            product_id = element[0],
            quantity = element[5]
        )
        print(transaction)
        session.add(transaction)
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

def create_user():
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    organisation = Organisation()
    organisation.name = "Schoggipopcorn"
    session.add(organisation)
    session.commit()

    user = User()
    user.email = "lukas.zimmermann@schoggipopcorn.ch"
    user.first_name = "Lukas"
    user.last_name = "Zimmermann"
    user.job_title = "Software Engineer"
    user.password_hash = pwd_context.hash("lukas")
    session.add(user)
    session.commit()

    user = session.query(User).filter_by(email="lukas.zimmermann@schoggipopcorn.ch").first()
    organisation = session.query(Organisation).filter_by(name="Schoggipopcorn").first()

    user_organisation = UserOrganisation()
    user_organisation.user = user
    user_organisation.organisation = organisation
    session.add(user_organisation)
    session.commit()



def main():
    # create_user()
    #import_category()
    #import_products()
    #import_supplier()
    #import_product_supplier()
    #import_unit()
    #import_attribute()
    #import_product_attribute()
    #import_price()
    #import_transaction()
    import_document()

if __name__ == "__main__":
    main()