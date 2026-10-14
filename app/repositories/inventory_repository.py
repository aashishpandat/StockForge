from app.extensions import db
from app.models.product import Product
from app.models.inventory_movement import InventoryMovement


class InventoryRepository:

    @staticmethod
    def get_product(product_id, lock=False):
        query = db.select(Product).where(Product.id == product_id)

        if lock:
            query = query.with_for_update()

        return db.session.execute(query).scalar_one_or_none()

    @staticmethod
    def create_movement(product_id, user_id, quantity, reason):
        movement = InventoryMovement(
            product_id=product_id,
            user_id=user_id,
            change_quantity=quantity,
            reason=reason
        )
        db.session.add(movement)
        return movement

    @staticmethod
    def create(movement):
        db.session.add(movement)
        return movement

    @staticmethod
    def commit():
        db.session.commit()

    @staticmethod
    def rollback():
        db.session.rollback()
