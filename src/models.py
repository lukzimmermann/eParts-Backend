from enum import Enum
from pydantic_core import Url
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, ForeignKeyConstraint, String, Integer, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()
metadata = Base.metadata

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    password_hash = Column(String(60), nullable=False)
    job_title = Column(String(50), nullable=True)
    create_at = Column(DateTime, default=func.now(), nullable=False)
    update_at = Column(DateTime, nullable=True)
    disabled = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"id: {self.id}, name: {self.email}, hash: {self.password_hash[:10]}..."
    
class Organisation(Base):
    __tablename__ = "organisation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    create_at = Column(DateTime, default=func.now(), nullable=False)


class UserOrganisation(Base):
    __tablename__ = "user_organisation"

    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    organisation_id = Column(Integer, ForeignKey('organisation.id', ondelete='CASCADE'), primary_key=True)
    join_date = Column(DateTime, default=func.now(), nullable=False)

    user = relationship("User", backref=backref("organisations", cascade="all, delete"))
    organisation = relationship("Organisation", backref=backref("users", cascade="all, delete"))

    def __repr__(self):
        return f"user_id: {self.user_id}, organisation_id: {self.organisation_id}, join_date: {self.join_date}"

    
class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, autoincrement=True)
    create_at = Column(DateTime, default=func.now(), nullable=False)
    update_at = Column(DateTime, nullable=True)
    name = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    manufacture = Column(String(255), nullable=False)
    manufacture_number = Column(String(255), nullable=False)
    minimum_quantity = Column(Float, nullable=True)

    #category = relationship("Category", back_populates="products")
    #suppliers = relationship("ProductSupplier", back_populates="product")
    #attributes = relationship("ProductAttribute", back_populates="product")

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}, category_id: {self.category_id}"

class Category(Base):
    __tablename__ = "category"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_id = Column(Integer, nullable=True)
    name = Column(String(255), nullable=False)

    #products = relationship("Product", back_populates="category")

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"
    
class Supplier(Base):
    __tablename__ = "supplier"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)

    #product_suppliers = relationship("ProductSupplier", back_populates="supplier")
    

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"

class ProductSupplier(Base):
    __tablename__ = "product_supplier"

    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True,nullable=False)
    supplier_id = Column(Integer, ForeignKey('supplier.id'), primary_key=True, nullable=False)
    number = Column(String(255) ,nullable=False)
    product_page = Column(String(2048), nullable=True)

    #supplier = relationship("Supplier", back_populates="product_suppliers")
    #product = relationship("Product", back_populates="suppliers")
    #price = relationship("Price", back_populates="product_supplier")

    def __repr__(self):
        return f"product id: {self.product_id}, supplier id: {self.supplier_id}, number: {self.number}, product page: {self.product_page[:20]}"

class Unit(Base):
    __tablename__ = "unit"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    parent_id = Column(Integer, nullable=True)
    name = Column(String(32), unique=True, nullable=False)
    factor = Column(Float, nullable=False)

    #attributes = relationship("Attribute", back_populates="unit")
    #product_attributes = relationship("ProductAttribute", back_populates="unit")

    def __repr__(self):
        return f"id: {self.id}, base id: {self.parent_id}, name: {self.name}, factor: {self.factor}"

class Attribute(Base):
    __tablename__ = "attribute"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    parent_id = Column(Integer, nullable=True)
    unit_id = Column(Integer, ForeignKey('unit.id'), nullable=True)
    name = Column(String(255), unique=True, nullable=False)
    isTitle = Column(Boolean, nullable=False, default=False)

    #unit = relationship("Unit", back_populates="attributes")
    #product_attributes = relationship("ProductAttribute", back_populates="attribute")

    def __repr__(self):
        return f"id: {self.id}, parent id: {self.parent_id}, unit id: {self.unit_id} name: {self.name}"
    
class ProductAttribute(Base):
    __tablename__ = "product_attribute"
    
    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True,nullable=False)
    unit_id = Column(Integer, ForeignKey('unit.id'), primary_key=True, nullable=False)
    attribute_id = Column(Integer, ForeignKey('attribute.id'), primary_key=True, nullable=False)
    text_value = Column(String(255), nullable=True)
    numeric_value = Column(Float, nullable=True)
    position = Column(Integer, nullable=True)

    #product = relationship("Product", back_populates="attributes")
    #attribute = relationship("Attribute", back_populates="product_attributes")
    #unit = relationship("Unit", back_populates="product_attributes")

    def __repr__(self):
        return f"id: {self.product_id}, unit id: {self.unit_id}, attribute id: {self.attribute_id} text_value: {self.text_value}, numeric_value: {self.numeric_value}"
    
class Price(Base):
    __tablename__ = "price"

    product_id = Column(Integer, primary_key=True, nullable=False)
    supplier_id = Column(Integer, primary_key=True, nullable=False)
    quantity = Column(Float, primary_key=True, nullable=False)
    price = Column(Float, nullable=False)

    # Composite foreign key referencing the composite primary key in product_supplier
    __table_args__ = (
        ForeignKeyConstraint(
            ['product_id', 'supplier_id'],
            ['product_supplier.product_id', 'product_supplier.supplier_id']
        ),
    )

    #product_supplier = relationship("ProductSupplier", back_populates="price")

    def __repr__(self):
        return f"Product Id: {self.product_id}, Supplier Id: {self.supplier_id}, Quantity: {self.quantity}, Price: {self.price}"

class ProductDocument(Base):
    __tablename__ = "product_document"

    id = Column(Integer, primary_key=True, nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True,nullable=False)
    description = Column(String(255), nullable=False)
    file_name = Column(String(255), nullable=False)

    def __repr__(self):
        return f"id: {self.id}, product id: {self.product_id}, description: {self.description}, file name: {self.file_name}"
    

class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Float, nullable=False)
    create_at = Column(DateTime, default=func.now(), nullable=False)

    def __repr__(self):
        return f'id: {self.id} product_id: {self.product_id} quantity: {self.quantity}'



class Log(Base):
    __tablename__ = "log"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    create_at = Column(DateTime, default=func.now(), nullable=False)
    level = Column(Integer, nullable=False)
    url = Column(String(512), nullable=True)
    method = Column(String(32), nullable=True)
    process_time = Column(Float, nullable=True)
    response_code = Column(Integer, nullable=True)
    user = Column(String(255), nullable=True)
    body = Column(String(4096), nullable=True)
    
    def __repr__(self):
        return f'id: {self.id} create_at: {self.create_at} level: {self.level} url: {self.url} method: {self.method} response_code: {self.response_code} process_time: {self.process_time}'