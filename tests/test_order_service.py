from app import create_app
from decimal import Decimal
from unittest.mock import patch, MagicMock

from app.services.order_service import create_order, cancel_order


@patch("app.services.order_service.OrderRepository.rollback")
def test_create_order_rejects_empty_items(mock_rollback):
    order, error, status_code = create_order(user_id=1, items=[])

    assert order is None
    assert error == "At least one item is required"
    assert status_code == 400


@patch("app.services.order_service.OrderRepository.rollback")
def test_create_order_rejects_invalid_product_id(mock_rollback):
    order, error, status_code = create_order(
        user_id=1,
        items=[{"product_id": 0, "quantity": 1}]
    )

    assert order is None
    assert error == "Each product_id must be a positive integer"
    assert status_code == 400


@patch("app.services.order_service.OrderRepository.rollback")
def test_create_order_rejects_invalid_quantity(mock_rollback):
    order, error, status_code = create_order(
        user_id=1,
        items=[{"product_id": 1, "quantity": 0}]
    )

    assert order is None
    assert error == "Each quantity must be a positive integer"
    assert status_code == 400



@patch("app.services.order_service.OrderRepository.create")
@patch("app.services.order_service.OrderRepository.get_product_for_update")
@patch("app.services.order_service.OrderRepository.rollback")
def test_create_order_rejects_insufficient_stock(
    mock_rollback,
    mock_get_product,
    mock_create_order,
    monkeypatch,
):
    # This is a unit test: use dummy settings and avoid connecting to MySQL.
    monkeypatch.setenv("SECRET_KEY", "test-secret-key")
    monkeypatch.setenv("JWT_SECRET_KEY", "test-jwt-secret-key")
    monkeypatch.setenv("DB_USER", "test-user")
    monkeypatch.setenv("DB_PASSWORD", "test-password")
    monkeypatch.setenv("DB_HOST", "127.0.0.1")
    monkeypatch.setenv("DB_PORT", "3306")
    monkeypatch.setenv("DB_NAME", "stockforge_test")

    app = create_app()

    product = MagicMock()
    product.id = 1
    product.is_active = True
    product.stock_quantity = 2
    mock_get_product.return_value = product

    with app.app_context():
        order, error, status_code = create_order(
            user_id=1,
            items=[{"product_id": 1, "quantity": 5}]
        )

    assert order is None
    assert "Insufficient stock" in error
    assert status_code == 409
    mock_rollback.assert_called_once()



@patch("app.services.order_service.OrderRepository.rollback")
@patch("app.services.order_service.OrderRepository.get_order_for_update")
def test_cancel_order_not_found(mock_get_order, mock_rollback):
    mock_get_order.return_value = None

    order, error, status_code = cancel_order(order_id=999, user_id=1)

    assert order is None
    assert error == "Order not found"
    assert status_code == 404
    mock_rollback.assert_called_once()


@patch("app.services.order_service.InventoryRepository.create_movement")
@patch("app.services.order_service.OrderRepository.commit")
@patch("app.services.order_service.OrderRepository.rollback")
@patch("app.services.order_service.OrderRepository.get_product_for_update")
@patch("app.services.order_service.OrderRepository.get_order_items")
@patch("app.services.order_service.OrderRepository.get_order_for_update")
def test_cancel_order_rolls_back_if_product_missing(
    mock_get_order, mock_get_items, mock_get_product, mock_rollback,
    mock_commit, mock_create_movement
):
    order = MagicMock()
    order.id = 10
    order.user_id = 1
    order.status = "Pending"
    item = MagicMock()
    item.product_id = 99
    item.quantity = 2
    mock_get_order.return_value = order
    mock_get_items.return_value = [item]
    mock_get_product.return_value = None

    result, error, status_code = cancel_order(order_id=10, user_id=1)

    assert result is None
    assert status_code == 409
    assert "product 99 is missing" in error
    mock_rollback.assert_called_once()
    mock_commit.assert_not_called()
    mock_create_movement.assert_not_called()
    assert order.status == "Pending"
