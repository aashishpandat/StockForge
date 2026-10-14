
from app.services.product_service import ProductService
from app.validations.product_validation import ProductValidation


class ProductController:

    @staticmethod
    def get_products():
        products = ProductService.get_active_products()

        return {
            "success": True,
            "count": len(products),
            "products": [
                {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "price": str(product.price),
                    "stock_quantity": product.stock_quantity
                }
                for product in products
            ]
        }, 200

    @staticmethod
    def create_product(data, user_id):
        validated_data, error = ProductValidation.validate_product(data)

        if error:
            return {
                "success": False,
                "message": error
            }, 400

        product, error, status_code = ProductService.create_product(
            validated_data, user_id
        )

        if error:
            return {
                "success": False,
                "message": error
            }, status_code

        return {
            "success": True,
            "message": "Product created successfully",
            "product": {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": str(product.price),
                "stock_quantity": product.stock_quantity
            }
        }, status_code
