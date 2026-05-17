from __future__ import annotations

import pytest

from backend.app import create_app
from backend.core.extensions import db
from backend.models.user import User
from backend.utils.jwt_utils import create_access_token


@pytest.fixture()
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def create_tables(app):
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def test_user(app):
    with app.app_context():
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        user_id = user.id
        username = user.username
    return {"id": user_id, "username": username}


@pytest.fixture()
def auth_headers(app, test_user):
    with app.app_context():
        token = create_access_token(test_user["id"])
    return {"Authorization": f"Bearer {token}"}
