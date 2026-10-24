
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.security import admin_required

from app.controllers.product_controller import ProductController

product_bp = Blueprint("products", __name__, url_prefix="/api/products")


@product_bp.route("", methods=["GET"])
def get_products():
    response, status_code = ProductController.get_products()
    return jsonify(response), status_code


@product_bp.route("", methods=["POST"])
@admin_required
def create_product():

    data = request.get_json(silent=True)
    user_id = int(get_jwt_identity())

    response, status_code = ProductController.create_product(
        data, user_id
    )

    return jsonify(response), status_code


@product_bp.route("/<int:product_id>", methods=["PATCH"])
@admin_required
def update_product(product_id):
    data = request.get_json(silent=True)
    response, status_code = ProductController.update_product(product_id, data)
    return jsonify(response), status_code


@product_bp.route("/<int:product_id>", methods=["DELETE"])
@admin_required
def deactivate_product(product_id):
    response, status_code = ProductController.deactivate_product(product_id)
    return jsonify(response), status_code
