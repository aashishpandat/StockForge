from app.extensions import db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product


class OrderRepository:

    @staticmethod
    def create(order):
        db.session.add(order)
        db.session.flush()
        return order

    @staticmethod
    def get_order_items_for_user(user_id):
        return (
            Order.query
            .filter_by(user_id=user_id)
            .order_by(Order.created_at.desc())
            .all()
        )


    @staticmethod
    def get_order_items_for_orders(order_ids):
        if not order_ids:
            return []

        return (
            OrderItem.query
            .filter(OrderItem.order_id.in_(order_ids))
            .all()
        )

    @staticmethod
    def get_product_for_update(product_id):
        return db.session.execute(
            db.select(Product)
            .where(Product.id == product_id)
            .with_for_update()
        ).scalar_one_or_none()

    @staticmethod
    def get_order_for_update(order_id):
        return db.session.execute(
            db.select(Order)
            .where(Order.id == order_id)
            .with_for_update()
        ).scalar_one_or_none()

    @staticmethod
    def get_order_items(order_id):
        return OrderItem.query.filter_by(order_id=order_id).all()

    @staticmethod
    def get_user_orders(user_id):
        return (
            Order.query
            .filter_by(user_id=user_id)
            .order_by(Order.created_at.desc())
            .all()
        )

    @staticmethod
    def db_session_add(record):
        db.session.add(record)

    @staticmethod
    def commit():
        db.session.commit()

    @staticmethod
    def rollback():
        db.session.rollback()
