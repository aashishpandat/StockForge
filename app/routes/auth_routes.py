from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token

from app.extensions import db
from app.models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"success": False, "message": "JSON object is required"}), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not all(isinstance(value, str) and value.strip() for value in [name, email, password]):
        return jsonify({"success": False, "message": "Name, email and password are required"}), 400

    name = name.strip()
    email = email.strip().lower()

    if len(name) > 100 or len(email) > 120:
        return jsonify({"success": False, "message": "Name or email is too long"}), 400

    if "@" not in email or "." not in email.split("@")[-1]:
        return jsonify({"success": False, "message": "Please provide a valid email address"}), 400

    if len(password) < 8:
        return jsonify({"success": False, "message": "Password must be at least 8 characters"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"success": False, "message": "Email is already registered"}), 409

    user = User(name=name, email=email, role="customer")
    user.set_password(password)

    db.session.add(user)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"success": False, "message": "Email is already registered"}), 409

    return jsonify({
        "success": True,
        "message": "Account created successfully",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"success": False, "message": "JSON object is required"}), 400

    email = data.get("email")
    password = data.get("password")

    if not isinstance(email, str) or not email.strip() or not isinstance(password, str) or not password:
        return jsonify({"success": False, "message": "Email and password are required"}), 400

    user = User.query.filter_by(email=email.strip().lower()).first()

    if not user or not user.check_password(password):
        return jsonify({"success": False, "message": "Invalid email or password"}), 401

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
    )

    return jsonify({
        "success": True,
        "message": "Login successful",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }), 200