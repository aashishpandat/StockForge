def validate_order_items(items):
    if not isinstance(items, list) or not items:
        return None, "At least one item is required"

    quantities = {}

    for item in items:
        if not isinstance(item, dict):
            return None, "Each item must be a JSON object"

        product_id = item.get("product_id")
        quantity = item.get("quantity")

        if (
            isinstance(product_id, bool)
            or not isinstance(product_id, int)
            or product_id <= 0
        ):
            return None, "Each product_id must be a positive integer"

        if (
            isinstance(quantity, bool)
            or not isinstance(quantity, int)
            or quantity <= 0
        ):
            return None, "Each quantity must be a positive integer"

        quantities[product_id] = (
            quantities.get(product_id, 0) + quantity
        )

    return quantities, None