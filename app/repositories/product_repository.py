
from app.extensions import db
from app.models.product import Product


class ProductRepository:

    @staticmethod
    def get_active_products():
        return (
            Product.query
            .filter_by(is_active=True)
            .order_by(Product.id.desc())
            .all()
        )

    @staticmethod
    def create(product):
        db.session.add(product)
        db.session.flush()
        return product

    @staticmethod
    def commit():
        db.session.commit()

    @staticmethod
    def rollback():
        db.session.rollback()
