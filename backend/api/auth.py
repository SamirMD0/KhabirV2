from __future__ import annotations

from flask import Blueprint, current_app, g, jsonify, make_response, request

from ..core.exceptions import AuthError
from ..schemas.auth_schemas import LoginSchema, SignupSchema
from ..services import auth_service
from ..utils.decorators import login_required
from ..utils.jwt_utils import create_access_token, decode_token

bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@bp.post("/signup")
def signup():
    data = SignupSchema().load(request.get_json(silent=True) or {})
    user = auth_service.signup(data["username"], data["email"], data["password"])
    return jsonify({"user_id": user.id, "username": user.username}), 201


@bp.post("/login")
def login():
    data = LoginSchema().load(request.get_json(silent=True) or {})
    user, access_token, refresh_token = auth_service.login(data["username"], data["password"])

    response = make_response(
        jsonify(
            {
                "access_token": access_token,
                "user_id": user.id,
                "username": user.username,
                "is_admin": user.is_admin,
            }
        )
    )
    response.set_cookie(
        current_app.config["REFRESH_COOKIE_NAME"],
        refresh_token,
        httponly=True,
        secure=not current_app.debug,
        samesite="Lax",
        max_age=current_app.config["REFRESH_COOKIE_MAX_AGE"],
    )
    return response


@bp.post("/logout")
def logout():
    response = make_response(jsonify({"success": True}))
    response.delete_cookie(current_app.config["REFRESH_COOKIE_NAME"])
    return response


@bp.post("/refresh")
def refresh():
    token = request.cookies.get(current_app.config["REFRESH_COOKIE_NAME"])
    if not token:
        raise AuthError("Missing refresh token")

    payload = decode_token(token)
    if payload.get("type") != "refresh":
        raise AuthError("Refresh token required")

    user = auth_service.get_user_from_token(token)
    return jsonify({"access_token": create_access_token(user.id)})


@bp.get("/me")
@login_required
def me():
    return jsonify(
        {
            "user_id": g.current_user.id,
            "username": g.current_user.username,
            "is_admin": g.current_user.is_admin,
        }
    )

