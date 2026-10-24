import os

from dotenv import load_dotenv
from flask import Flask, jsonify
from sqlalchemy import URL
from datetime import timedelta

from app.extensions import db, jwt

load_dotenv()


def create_app():
    app = Flask(__name__)

    required_settings = [
        "SECRET_KEY",
        "JWT_SECRET_KEY",
        "DB_USER",
        "DB_PASSWORD",
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
    ]

    missing_settings = [
        setting for setting in required_settings
        if not os.getenv(setting)
    ]

    if missing_settings:
        raise RuntimeError(
            "Missing required environment settings: "
            + ", ".join(missing_settings)
        )

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_HEADER_TYPE"] = "Bearer"
    app.config["JWT_ERROR_MESSAGE_KEY"] = "message"

    app.config["SQLALCHEMY_DATABASE_URI"] = URL.create(
        drivername="mysql+pymysql",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME"),
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    jwt.init_app(app)

    @app.errorhandler(404)
    def handle_not_found(_error):
        return jsonify({"success": False, "message": "Resource not found"}), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(_error):
        return jsonify({"success": False, "message": "Method not allowed"}), 405

    @app.errorhandler(500)
    def handle_internal_error(_error):
        db.session.rollback()
        return jsonify({"success": False, "message": "Internal server error"}), 500

    @jwt.unauthorized_loader
    def handle_missing_token(_reason):
        return jsonify({"success": False, "message": "Authorization token is required"}), 401

    @jwt.invalid_token_loader
    def handle_invalid_token(_reason):
        return jsonify({"success": False, "message": "Invalid authorization token"}), 401

    @jwt.expired_token_loader
    def handle_expired_token(_jwt_header, _jwt_payload):
        return jsonify({"success": False, "message": "Authorization token has expired"}), 401

    from app.routes.auth_routes import auth_bp
    from app.routes.product_routes import product_bp
    from app.routes.inventory_routes import inventory_bp
    from app.routes.order_routes import order_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(order_bp)

    return app