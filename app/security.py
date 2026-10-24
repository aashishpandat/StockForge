from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt, jwt_required


def admin_required(fn):
    """Require a valid access token whose role claim is admin."""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        if get_jwt().get("role") != "admin":
            return jsonify({
                "success": False,
                "message": "Admin access required"
            }), 403
        return fn(*args, **kwargs)

    return wrapper
