from models import Price, Product, ProductSupplier, Supplier
from routes.product.productDto import PriceDto, ProductDto, SupplierDto, SupplierProductDto
from utils.database import Database


session = Database().get_session()

def get_product_from_db(product_id) -> Product:
    product = session.query(Product).where(Product.id == product_id).one_or_none()
    suppliers = get_suppliers_of_product(product.id)
    return ProductDto(
        id=product.id,
        create_at=product.create_at,
        update_at=product.update_at,
        name=product.name,
        category_id=product.category_id,
        manufacture=product.manufacture,
        manufacture_number=product.manufacture_number,
        minimum_quantity=product.minimum_quantity,
        suppliers=suppliers
        )


def get_suppliers_of_product(product_id):
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



