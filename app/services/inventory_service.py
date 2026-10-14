from app.repositories.inventory_repository import InventoryRepository


def adjust_stock(product_id, user_id, change_quantity, reason):
    try:
        product = InventoryRepository.get_product(product_id, lock=True)

        if not product or not product.is_active:
            InventoryRepository.rollback()
            return None, {
                "success": False,
                "message": "Product not found"
            }, 404

        previous_stock = product.stock_quantity
        new_quantity = previous_stock + change_quantity

        if new_quantity < 0:
            InventoryRepository.rollback()
            return None, {
                "success": False,
                "message": "Insufficient stock for this adjustment",
                "available_stock": previous_stock
            }, 409

        product.stock_quantity = new_quantity

        InventoryRepository.create_movement(
            product_id=product.id,
            user_id=user_id,
            quantity=change_quantity,
            reason=reason
        )

        InventoryRepository.commit()

        return {
            "id": product.id,
            "name": product.name,
            "previous_stock": previous_stock,
            "change_quantity": change_quantity,
            "current_stock": product.stock_quantity
        }, None, 200

    except Exception:
        InventoryRepository.rollback()
        return None, {
            "success": False,
            "message": "Stock adjustment failed"
        }, 500