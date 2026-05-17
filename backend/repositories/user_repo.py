from __future__ import annotations

from ..core.extensions import db
from ..models.user import User


def get_by_id(id: int) -> User | None:
    return db.session.get(User, id)


def get_by_username(username: str) -> User | None:
    return User.query.filter_by(username=username).first()


def get_by_email(email: str) -> User | None:
    return User.query.filter_by(email=email).first()


def create(user: User) -> User:
    db.session.add(user)
    save()
    return user


def save() -> None:
    db.session.commit()

