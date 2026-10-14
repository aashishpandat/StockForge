from app.validations.order_validation import validate_order_items


def test_valid_order_items():
    quantities, error = validate_order_items([
        {"product_id": 1, "quantity": 2},
        {"product_id": 2, "quantity": 1}
    ])

    assert error is None
    assert quantities == {1: 2, 2: 1}


def test_empty_order_items():
    quantities, error = validate_order_items([])

    assert quantities is None
    assert error == "At least one item is required"


def test_invalid_product_id():
    quantities, error = validate_order_items([
        {"product_id": 0, "quantity": 1}
    ])

    assert quantities is None
    assert error == "Each product_id must be a positive integer"


def test_invalid_quantity():
    quantities, error = validate_order_items([
        {"product_id": 1, "quantity": 0}
    ])

    assert quantities is None
    assert error == "Each quantity must be a positive integer"


def test_non_object_item():
    quantities, error = validate_order_items(["invalid"])

    assert quantities is None
    assert error == "Each item must be a JSON object"


def test_duplicate_products_are_combined():
    quantities, error = validate_order_items([
        {"product_id": 1, "quantity": 2},
        {"product_id": 1, "quantity": 3}
    ])

    assert error is None
    assert quantities == {1: 5}


def test_boolean_values_are_rejected():
    quantities, error = validate_order_items([
        {"product_id": True, "quantity": 1}
    ])

    assert quantities is None
    assert error == "Each product_id must be a positive integer"