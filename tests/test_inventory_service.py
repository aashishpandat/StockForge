
from unittest.mock import patch, Mock

from app.services.inventory_service import adjust_stock


def make_product(stock_quantity=35, is_active=True):
    product = Mock()
    product.id = 1
    product.name = "Wireless Mouse"
    product.stock_quantity = stock_quantity
    product.is_active = is_active
    return product


@patch("app.services.inventory_service.InventoryRepository.commit")
@patch("app.services.inventory_service.InventoryRepository.create_movement")
@patch("app.services.inventory_service.InventoryRepository.get_product")
def test_adjust_stock_success(mock_get_product, mock_create_movement, mock_commit):
    product = make_product(stock_quantity=35)
    mock_get_product.return_value = product

    result, error, status_code = adjust_stock(
        product_id=1,
        user_id=2,
        change_quantity=5,
        reason="Stock replenishment"
    )

    assert status_code == 200
    assert error is None
    assert result["previous_stock"] == 35
    assert result["current_stock"] == 40
    assert product.stock_quantity == 40
    mock_create_movement.assert_called_once_with(
        product_id=1,
        user_id=2,
        quantity=5,
        reason="Stock replenishment"
    )
    mock_commit.assert_called_once()


@patch("app.services.inventory_service.InventoryRepository.rollback")
@patch("app.services.inventory_service.InventoryRepository.get_product")
def test_adjust_stock_product_not_found(mock_get_product, mock_rollback):
    mock_get_product.return_value = None

    result, error, status_code = adjust_stock(1, 2, 5, "Restock")

    assert result is None
    assert status_code == 404
    assert error["message"] == "Product not found"
    mock_rollback.assert_called_once()


@patch("app.services.inventory_service.InventoryRepository.rollback")
@patch("app.services.inventory_service.InventoryRepository.get_product")
def test_adjust_stock_inactive_product(mock_get_product, mock_rollback):
    mock_get_product.return_value = make_product(is_active=False)

    result, error, status_code = adjust_stock(1, 2, 5, "Restock")

    assert result is None
    assert status_code == 404
    assert error["message"] == "Product not found"
    mock_rollback.assert_called_once()


@patch("app.services.inventory_service.InventoryRepository.rollback")
@patch("app.services.inventory_service.InventoryRepository.commit")
@patch("app.services.inventory_service.InventoryRepository.create_movement")
@patch("app.services.inventory_service.InventoryRepository.get_product")
def test_adjust_stock_insufficient_stock(
    mock_get_product, mock_create_movement, mock_commit, mock_rollback
):
    product = make_product(stock_quantity=35)
    mock_get_product.return_value = product

    result, error, status_code = adjust_stock(
        1, 2, -100, "Stock correction"
    )

    assert result is None
    assert status_code == 409
    assert error["message"] == "Insufficient stock for this adjustment"
    assert error["available_stock"] == 35
    assert product.stock_quantity == 35
    mock_create_movement.assert_not_called()
    mock_commit.assert_not_called()
    mock_rollback.assert_called_once()


@patch("app.services.inventory_service.InventoryRepository.rollback")
@patch(
    "app.services.inventory_service.InventoryRepository.commit",
    side_effect=Exception("Database error")
)
@patch("app.services.inventory_service.InventoryRepository.create_movement")
@patch("app.services.inventory_service.InventoryRepository.get_product")
def test_adjust_stock_database_failure(
    mock_get_product, mock_create_movement, mock_commit, mock_rollback
):
    product = make_product(stock_quantity=35)
    mock_get_product.return_value = product

    result, error, status_code = adjust_stock(
        1, 2, 5, "Stock replenishment"
    )

    assert result is None
    assert status_code == 500
    assert error["message"] == "Stock adjustment failed"
    mock_rollback.assert_called_once()
