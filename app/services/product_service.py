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


    @staticmethod
    def update_product(product_id, data):
        try:
            product = ProductRepository.get_by_id(product_id)
            if not product or not product.is_active:
                return None, "Product not found", 404

            if "name" in data:
                product.name = data["name"]
            if "description" in data:
                product.description = data["description"]
            if "price" in data:
                product.price = data["price"]
            ProductRepository.commit()
            return product, None, 200
        except Exception:
            ProductRepository.rollback()
            return None, "Product could not be updated", 500

    @staticmethod
    def deactivate_product(product_id):
        try:
            product = ProductRepository.get_by_id(product_id)
            if not product or not product.is_active:
                return None, "Product not found", 404

            product.is_active = False
            ProductRepository.commit()
            return product, None, 200
        except Exception:
            ProductRepository.rollback()
            return None, "Product could not be deactivated", 500
