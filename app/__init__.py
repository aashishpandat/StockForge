import os

from dotenv import load_dotenv
from flask import Flask
from sqlalchemy import URL

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

    from app.routes.auth_routes import auth_bp
    from app.routes.product_routes import product_bp
    from app.routes.inventory_routes import inventory_bp
    from app.routes.order_routes import order_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(order_bp)

    return app