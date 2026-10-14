from app.repositories.order_repository import OrderRepository
from app.services.order_service import create_order, cancel_order


def place_order_controller(user_id, items):
    order, error, status_code = create_order(user_id, items)

    if error:
        return {
            "success": False,
            "message": error
        }, status_code

    return {
        "success": True,
        "message": "Order placed successfully",
        "order": {
            "id": order.id,
            "total_amount": str(order.total_amount),
            "status": order.status
        }
    }, 201


def get_my_orders_controller(user_id):
    orders = OrderRepository.get_order_items_for_user(user_id)

    order_ids = [order.id for order in orders]
    items = OrderRepository.get_order_items_for_orders(order_ids)

    items_by_order = {}

    for item in items:
        items_by_order.setdefault(item.order_id, []).append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "unit_price": str(item.unit_price)
        })

    formatted_orders = [
        {
            "id": order.id,
            "total_amount": str(order.total_amount),
            "status": order.status,
            "items": items_by_order.get(order.id, []),
            "created_at": order.created_at.isoformat()
        }
        for order in orders
    ]

    return {
        "success": True,
        "count": len(formatted_orders),
        "orders": formatted_orders
    }, 200

def cancel_order_controller(order_id, user_id):
    order, error, status_code = cancel_order(order_id, user_id)

    if error:
        return {
            "success": False,
            "message": error
        }, status_code

    return {
        "success": True,
        "message": "Order cancelled successfully",
        "order": {
            "id": order.id,
            "status": order.status,
            "total_amount": str(order.total_amount)
        }
    }, 200