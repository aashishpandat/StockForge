def validate_stock_adjustment(data):
    if not isinstance(data, dict):
        return None, "JSON object is required"

    change_quantity = data.get("change_quantity")
    reason = data.get("reason")

    if (
        isinstance(change_quantity, bool)
        or not isinstance(change_quantity, int)
    ):
        return None, "change_quantity must be a whole number"

    if change_quantity == 0:
        return None, "Stock change cannot be zero"

    if not isinstance(reason, str) or not reason.strip():
        return None, "A reason for the adjustment is required"

    reason = reason.strip()

    if len(reason) > 200:
        return None, "Reason cannot exceed 200 characters"

    return {
        "change_quantity": change_quantity,
        "reason": reason
    }, None