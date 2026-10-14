
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from app.controllers.product_controller import ProductController

product_bp = Blueprint("products", __name__, url_prefix="/api/products")


@product_bp.route("", methods=["GET"])
def get_products():
    response, status_code = ProductController.get_products()
    return jsonify(response), status_code


@product_bp.route("", methods=["POST"])
@jwt_required()
def create_product():
    if get_jwt().get("role") != "admin":
        return jsonify({
            "success": False,
            "message": "Admin access required"
        }), 403

    data = request.get_json(silent=True)
    user_id = int(get_jwt_identity())

    response, status_code = ProductController.create_product(
        data, user_id
    )

    return jsonify(response), status_code
