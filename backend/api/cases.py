from __future__ import annotations

from flask import Blueprint, jsonify

bp = Blueprint("cases", __name__, url_prefix="/api/cases")


@bp.get("/")
def index():
    return jsonify({"message": "Cases API TODO"})

