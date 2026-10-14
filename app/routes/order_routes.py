
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.controllers.order_controller import (
    place_order_controller,
    get_my_orders_controller,
    cancel_order_controller,
)


order_bp = Blueprint("orders", __name__, url_prefix="/api/orders")


@order_bp.route("", methods=["POST"])
@jwt_required()
def place_order():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "message": "JSON object is required"
        }), 400

    user_id = int(get_jwt_identity())
    items = data.get("items")

    response, status_code = place_order_controller(user_id, items)

    return jsonify(response), status_code


@order_bp.route("", methods=["GET"])
@jwt_required()
def get_my_orders():
    user_id = int(get_jwt_identity())

    response, status_code = get_my_orders_controller(user_id)

    return jsonify(response), status_code


@order_bp.route("/<int:order_id>/cancel", methods=["PATCH"])
@jwt_required()
def cancel_my_order(order_id):
    user_id = int(get_jwt_identity())

    response, status_code = cancel_order_controller(order_id, user_id)

    return jsonify(response), status_code
