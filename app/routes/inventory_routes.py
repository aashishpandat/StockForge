
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from app.controllers.inventory_controller import adjust_stock_controller

inventory_bp = Blueprint(
    "inventory",
    __name__,
    url_prefix="/api/inventory"
)


@inventory_bp.route("/<int:product_id>/adjust", methods=["PATCH"])
@jwt_required()
def adjust_stock_route(product_id):
    if get_jwt().get("role") != "admin":
        return jsonify({
            "success": False,
            "message": "Admin access required"
        }), 403

    data = request.get_json(silent=True)

    response, status_code = adjust_stock_controller(
        product_id=product_id,
        user_id=int(get_jwt_identity()),
        data=data
    )

    return jsonify(response), status_code
