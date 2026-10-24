
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.security import admin_required

from app.controllers.inventory_controller import adjust_stock_controller

inventory_bp = Blueprint(
    "inventory",
    __name__,
    url_prefix="/api/inventory"
)


@inventory_bp.route("/<int:product_id>/adjust", methods=["PATCH"])
@admin_required
def adjust_stock_route(product_id):

    data = request.get_json(silent=True)

    response, status_code = adjust_stock_controller(
        product_id=product_id,
        user_id=int(get_jwt_identity()),
        data=data
    )

    return jsonify(response), status_code
