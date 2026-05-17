from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from flask import current_app
from jwt import InvalidTokenError

from ..core.exceptions import AuthError


def _create_token(user_id: int, expires_seconds: int, token_type: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "type": token_type,
        "iat": now,
        "exp": now + timedelta(seconds=expires_seconds),
    }
    return jwt.encode(payload, current_app.config["JWT_SECRET_KEY"], algorithm="HS256")


def create_access_token(user_id: int) -> str:
    return _create_token(user_id, current_app.config["JWT_ACCESS_TOKEN_EXPIRES"], "access")


def create_refresh_token(user_id: int) -> str:
    return _create_token(user_id, current_app.config["JWT_REFRESH_TOKEN_EXPIRES"], "refresh")


def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
    except InvalidTokenError as exc:
        raise AuthError("Invalid or expired token") from exc

