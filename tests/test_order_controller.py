
from unittest.mock import patch, MagicMock

from app.controllers.order_controller import (
    place_order_controller,
    get_my_orders_controller,
    cancel_order_controller,
)


@patch("app.controllers.order_controller.create_order")
def test_place_order_success(mock_create_order):
    order = MagicMock()
    order.id = 1
    order.total_amount = "799.00"
    order.status = "Pending"
    mock_create_order.return_value = (order, None, 201)

    response, status_code = place_order_controller(
        user_id=1,
        items=[{"product_id": 1, "quantity": 1}]
    )

    assert status_code == 201
    assert response["success"] is True
    assert response["order"]["id"] == 1


@patch(
    "app.controllers.order_controller.OrderRepository.get_order_items_for_user"
)
@patch(
    "app.controllers.order_controller.OrderRepository.get_order_items_for_orders"
)
def test_get_my_orders_success(mock_get_items, mock_get_orders):
    from datetime import datetime
    from decimal import Decimal
    from types import SimpleNamespace

    order = SimpleNamespace(
        id=1,
        total_amount=Decimal("799.00"),
        status="Pending",
        created_at=datetime(2026, 10, 13, 10, 0, 0)
    )

    mock_get_orders.return_value = [order]
    mock_get_items.return_value = []

    response, status_code = get_my_orders_controller(user_id=1)

    assert status_code == 200
    assert response["success"] is True
    assert response["count"] == 1
    assert response["orders"][0]["id"] == 1
    assert response["orders"][0]["items"] == []

@patch("app.controllers.order_controller.cancel_order")
def test_cancel_order_not_found(mock_cancel_order):
    mock_cancel_order.return_value = (None, "Order not found", 404)

    response, status_code = cancel_order_controller(
        order_id=999,
        user_id=1
    )

    assert status_code == 404
    assert response["success"] is False
    assert response["message"] == "Order not found"
