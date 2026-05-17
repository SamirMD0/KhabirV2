from __future__ import annotations

from ..core.exceptions import AuthError, ValidationError
from ..models.user import User
from ..repositories import user_repo
from ..utils.jwt_utils import create_access_token, create_refresh_token, decode_token


def signup(username: str, email: str, password: str) -> User:
    if user_repo.get_by_username(username):
        raise ValidationError("Username already exists")
    if user_repo.get_by_email(email):
        raise ValidationError("Email already exists")

    user = User(username=username, email=email)
    user.set_password(password)
    return user_repo.create(user)


def login(username: str, password: str) -> tuple[User, str, str]:
    user = user_repo.get_by_username(username)
    if user is None or not user.check_password(password):
        raise AuthError("Invalid username or password")
    if not user.is_active:
        raise AuthError("User account is inactive")

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    return user, access_token, refresh_token


def get_user_from_token(token: str) -> User:
    payload = decode_token(token)
    user = user_repo.get_by_id(int(payload["sub"]))
    if user is None or not user.is_active:
        raise AuthError("User not found or inactive")
    return user

