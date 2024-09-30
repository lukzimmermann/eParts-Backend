from pydantic_core import Url
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, ForeignKeyConstraint, String, Integer, Text, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(60), nullable=False)
    create_at = Column(DateTime, default=func.now(), nullable=False)
    update_at = Column(DateTime, nullable=True)
    disabled = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}, hash: {self.password_hash[:10]}..."
    

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
        return f"id: {self.id}, base id: {self.parent_id}, name: {self.name}"


class Attribute(Base):
    __tablename__ = "attribute"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    parent_id = Column(Integer, nullable=True)
    unit_id = Column(Integer, ForeignKey('unit.id'), nullable=False)
    name = Column(String(255), unique=True, nullable=False)

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