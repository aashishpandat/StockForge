
from app.services.inventory_service import adjust_stock


def adjust_stock_controller(product_id, user_id, data):
    from app.validations.inventory_validation import validate_stock_adjustment

    validated_data, error = validate_stock_adjustment(data)

    if error:
        return {
            "success": False,
            "message": error
        }, 400

    product, error_response, status_code = adjust_stock(
        product_id=product_id,
        user_id=user_id,
        change_quantity=validated_data["change_quantity"],
        reason=validated_data["reason"]
    )

    if error_response:
        return error_response, status_code

    return {
        "success": True,
        "message": "Stock adjusted successfully",
        "product": product
    }, status_code
