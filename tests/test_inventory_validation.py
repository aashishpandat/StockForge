
from app.validations.inventory_validation import validate_stock_adjustment


def test_valid_stock_adjustment():
    data, error = validate_stock_adjustment({
        "change_quantity": 5,
        "reason": "  Stock replenishment  "
    })

    assert error is None
    assert data == {
        "change_quantity": 5,
        "reason": "Stock replenishment"
    }


def test_stock_adjustment_requires_json_object():
    data, error = validate_stock_adjustment(None)

    assert data is None
    assert error == "JSON object is required"


def test_change_quantity_must_be_integer():
    data, error = validate_stock_adjustment({
        "change_quantity": 2.5,
        "reason": "Stock correction"
    })

    assert data is None
    assert error == "change_quantity must be a whole number"


def test_boolean_quantity_is_rejected():
    data, error = validate_stock_adjustment({
        "change_quantity": True,
        "reason": "Stock correction"
    })

    assert data is None
    assert error == "change_quantity must be a whole number"


def test_zero_quantity_is_rejected():
    data, error = validate_stock_adjustment({
        "change_quantity": 0,
        "reason": "Stock correction"
    })

    assert data is None
    assert error == "Stock change cannot be zero"


def test_empty_reason_is_rejected():
    data, error = validate_stock_adjustment({
        "change_quantity": 5,
        "reason": "   "
    })

    assert data is None
    assert error == "A reason for the adjustment is required"


def test_reason_over_200_characters_is_rejected():
    data, error = validate_stock_adjustment({
        "change_quantity": 5,
        "reason": "a" * 201
    })

    assert data is None
    assert error == "Reason cannot exceed 200 characters"
