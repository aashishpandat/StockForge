from decimal import Decimal

from app.models.order import Order
from app.models.order_item import OrderItem
from app.repositories.order_repository import OrderRepository
from app.repositories.inventory_repository import InventoryRepository
from app.validations.order_validation import validate_order_items
import logging

logger = logging.getLogger(__name__)


def create_order(user_id, items):
    quantities, validation_error = validate_order_items(items)

    if validation_error:
        return None, validation_error, 400

    try:
        order = Order(
            user_id=user_id,
            total_amount=Decimal("0.00")
        )
        OrderRepository.create(order)

        total_amount = Decimal("0.00")

        for product_id, quantity in quantities.items():
            product = OrderRepository.get_product_for_update(product_id)

            if not product or not product.is_active:
                OrderRepository.rollback()
                return None, f"Product {product_id} not found", 404

            if product.stock_quantity < quantity:
                available = product.stock_quantity
                OrderRepository.rollback()
                return None, (
                    f"Insufficient stock for product {product_id}. "
                    f"Available stock: {available}"
                ), 409

            unit_price = Decimal(str(product.price))
            total_amount += unit_price * quantity
            product.stock_quantity -= quantity

            db_order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=unit_price
            )
            OrderRepository.db_session_add(db_order_item)

            InventoryRepository.create_movement(
                product_id=product.id,
                user_id=user_id,
                quantity=-quantity,
                reason=f"Order #{order.id}"
            )

        order.total_amount = total_amount
        OrderRepository.commit()

        return order, None, 201

    except Exception as e:
        logger.exception("Failed to create order")
        OrderRepository.rollback()
        return None, "Order could not be created", 500


def cancel_order(order_id, user_id):
    try:
        order = OrderRepository.get_order_for_update(order_id)

        if not order:
            OrderRepository.rollback()
            return None, "Order not found", 404

        if order.user_id != user_id:
            OrderRepository.rollback()
            return None, "You cannot cancel this order", 403

        if order.status != "Pending":
            OrderRepository.rollback()
            return None, "Only pending orders can be cancelled", 409

        items = OrderRepository.get_order_items(order.id)

        for item in items:
            product = OrderRepository.get_product_for_update(item.product_id)

            if not product:
                OrderRepository.rollback()
                return None, (
                    f"Cannot cancel order because product {item.product_id} "
                    "is missing; inventory was not changed"
                ), 409

            product.stock_quantity += item.quantity

            InventoryRepository.create_movement(
                product_id=product.id,
                user_id=user_id,
                quantity=item.quantity,
                reason=f"Cancellation of Order #{order.id}"
            )

        order.status = "Cancelled"
        OrderRepository.commit()

        return order, None, 200

    except Exception as e:
        logger.exception("Failed to cancel order")
        OrderRepository.rollback()
        return None, "Order could not be cancelled", 500