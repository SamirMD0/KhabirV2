from __future__ import annotations

from flask import Blueprint, jsonify

bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@bp.get("/")
def index():
    return jsonify({"message": "Admin API TODO"})

