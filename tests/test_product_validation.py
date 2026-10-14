
import pytest

from app.validations.product_validation import ProductValidation


def test_valid_product():
    data = {
        "name": "Wireless Mouse",
        "description": "Wireless mouse for daily use",
        "price": 799,
        "stock_quantity": 35
    }

    validated_data, error = ProductValidation.validate_product(data)

    assert error is None
    assert validated_data["name"] == "Wireless Mouse"
    assert validated_data["stock_quantity"] == 35


def test_missing_product_name():
    data = {
        "description": "Test product",
        "price": 499,
        "stock_quantity": 5
    }

    validated_data, error = ProductValidation.validate_product(data)

    assert validated_data is None
    assert error == "A valid product name is required"


def test_invalid_product_price():
    data = {
        "name": "Test Product",
        "price": -100,
        "stock_quantity": 5
    }

    validated_data, error = ProductValidation.validate_product(data)

    assert validated_data is None
    assert error == "Price must be positive and within the allowed range"


def test_invalid_stock_quantity():
    data = {
        "name": "Test Product",
        "price": 499,
        "stock_quantity": -1
    }

    validated_data, error = ProductValidation.validate_product(data)

    assert validated_data is None
    assert error == "Stock quantity is out of range"


def test_boolean_price_is_rejected():
    data = {
        "name": "Test Product",
        "price": True,
        "stock_quantity": 5
    }

    validated_data, error = ProductValidation.validate_product(data)

    assert validated_data is None
    assert error == "A valid price is required"
