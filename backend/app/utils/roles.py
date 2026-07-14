from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request


def require_role(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            if get_jwt().get("rol") not in roles:
                return jsonify({"error": "No tenes permisos para esta accion"}), 403
            return fn(*args, **kwargs)

        return wrapper

    return decorator
