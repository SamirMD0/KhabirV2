from __future__ import annotations

import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me-generate-with-secrets-token-hex-32")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "get-free-key-at-aistudio.google.com")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me-another-random-32-hex")
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "900"))
    JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", "604800"))
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "backend/static/uploads")
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", "16777216"))
    RATELIMIT_DEFAULT = os.getenv("RATELIMIT_DEFAULT", "200/day;50/hour")
    REFRESH_COOKIE_NAME = "refresh_token"
    REFRESH_COOKIE_MAX_AGE = JWT_REFRESH_TOKEN_EXPIRES
    PERMANENT_SESSION_LIFETIME = timedelta(seconds=JWT_REFRESH_TOKEN_EXPIRES)


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///khabir.db"


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    RATELIMIT_ENABLED = False


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def get_config(config_name: str | None = None) -> type[BaseConfig]:
    env_name = config_name or os.getenv("FLASK_ENV", "development")
    return config_by_name.get(env_name, DevelopmentConfig)

