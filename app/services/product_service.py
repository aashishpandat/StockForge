from app.repositories.inventory_repository import InventoryRepository
from app.models.product import Product
from app.models.inventory_movement import InventoryMovement
from app.repositories.product_repository import ProductRepository


class ProductService:

    @staticmethod
    def get_active_products():
        return ProductRepository.get_active_products()

    @staticmethod
    def create_product(data, user_id):
        try:
            product = Product(
                name=data["name"],
                description=data["description"],
                price=data["price"],
                stock_quantity=data["stock_quantity"]
            )

            ProductRepository.create(product)

            if data["stock_quantity"] > 0:
                movement = InventoryMovement(
                    product_id=product.id,
                    user_id=user_id,
                    change_quantity=data["stock_quantity"],
                    reason="Initial stock"
                )
                InventoryRepository.create(movement)

            ProductRepository.commit()
            return product, None, 201

        except Exception:
            ProductRepository.rollback()
            return None, "Product could not be created", 500
