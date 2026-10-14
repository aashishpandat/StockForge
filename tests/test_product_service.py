
from unittest.mock import patch

from app.services.product_service import ProductService


def test_create_product_success():
    data = {
        "name": "Test Keyboard",
        "description": "Mechanical keyboard",
        "price": 2499,
        "stock_quantity": 10
    }

    with patch(
        "app.services.product_service.ProductRepository.create"
    ) as mock_create, patch(
        "app.services.product_service.ProductRepository.commit"
    ) as mock_commit, patch(
        "app.services.product_service.InventoryRepository.create"
    ) as mock_inventory_create:

        product, error, status_code = ProductService.create_product(
            data, user_id=1
        )

        assert error is None
        assert status_code == 201
        assert product.name == "Test Keyboard"
        assert product.stock_quantity == 10

        mock_create.assert_called_once()
        mock_inventory_create.assert_called_once()
        mock_commit.assert_called_once()


def test_create_product_without_initial_stock():
    data = {
        "name": "Test Mouse",
        "description": "Wireless mouse",
        "price": 799,
        "stock_quantity": 0
    }

    with patch(
        "app.services.product_service.ProductRepository.create"
    ) as mock_create, patch(
        "app.services.product_service.ProductRepository.commit"
    ) as mock_commit, patch(
        "app.services.product_service.InventoryRepository.create"
    ) as mock_inventory_create:

        product, error, status_code = ProductService.create_product(
            data, user_id=1
        )

        assert error is None
        assert status_code == 201
        assert product.name == "Test Mouse"

        mock_create.assert_called_once()
        mock_inventory_create.assert_not_called()
        mock_commit.assert_called_once()


def test_create_product_database_failure():
    data = {
        "name": "Failure Product",
        "description": "Test database failure",
        "price": 100,
        "stock_quantity": 5
    }

    with patch(
        "app.services.product_service.ProductRepository.create",
        side_effect=Exception("Database error")
    ), patch(
        "app.services.product_service.ProductRepository.rollback"
    ) as mock_rollback:

        product, error, status_code = ProductService.create_product(
            data, user_id=1
        )

        assert product is None
        assert error == "Product could not be created"
        assert status_code == 500
        mock_rollback.assert_called_once()
