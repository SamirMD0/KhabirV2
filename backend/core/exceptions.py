from __future__ import annotations

from http import HTTPStatus
from typing import Any

from flask import Flask, jsonify
from marshmallow import ValidationError as MarshmallowValidationError


class AppError(Exception):
    status_code = HTTPStatus.BAD_REQUEST
    message = "Request failed"

    def __init__(self, message: str | None = None, details: Any | None = None) -> None:
        super().__init__(message or self.message)
        self.message = message or self.message
        self.details = details


class AuthError(AppError):
    status_code = HTTPStatus.UNAUTHORIZED
    message = "Authentication failed"


class NotFoundError(AppError):
    status_code = HTTPStatus.NOT_FOUND
    message = "Resource not found"


class ForbiddenError(AppError):
    status_code = HTTPStatus.FORBIDDEN
    message = "Forbidden"


class ValidationError(AppError):
    status_code = HTTPStatus.BAD_REQUEST
    message = "Validation failed"


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(AppError)
    def handle_app_error(error: AppError):
        payload: dict[str, Any] = {"error": error.message}
        if error.details is not None:
            payload["details"] = error.details
        return jsonify(payload), int(error.status_code)

    @app.errorhandler(MarshmallowValidationError)
    def handle_marshmallow_error(error: MarshmallowValidationError):
        return jsonify({"error": "Validation failed", "details": error.messages}), 400

    @app.errorhandler(404)
    def handle_not_found(_: Exception):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(_: Exception):
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(Exception)
    def handle_unexpected(error: Exception):
        if app.debug:
            raise error
        return jsonify({"error": "Internal server error"}), 500

