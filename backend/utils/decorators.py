from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import Any

from flask import g, request

from ..core.exceptions import AuthError, ForbiddenError
from ..repositories import user_repo
from .jwt_utils import decode_token


def _load_current_user() -> None:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise AuthError("Missing bearer token")

    token = auth_header.removeprefix("Bearer ").strip()
    payload = decode_token(token)
    if payload.get("type") != "access":
        raise AuthError("Access token required")

    user = user_repo.get_by_id(int(payload["sub"]))
    if user is None or not user.is_active:
        raise AuthError("User not found or inactive")

    g.current_user = user


def login_required(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        _load_current_user()
        return func(*args, **kwargs)

    return wrapper


def admin_required(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        _load_current_user()
        if not g.current_user.is_admin:
            raise ForbiddenError("Admin privileges required")
        return func(*args, **kwargs)

    return wrapper

