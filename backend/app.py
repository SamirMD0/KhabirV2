from __future__ import annotations

from flask import Flask, jsonify, render_template

from .api.admin import bp as admin_bp
from .api.auth import bp as auth_bp
from .api.cases import bp as cases_bp
from .api.health import bp as health_bp
from .core.config import get_config
from .core.exceptions import register_error_handlers
from .core.extensions import cors, db, limiter, migrate


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, supports_credentials=True)
    limiter.init_app(app)

    register_error_handlers(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(cases_bp)
    app.register_blueprint(admin_bp)

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/api")
    def api_root():
        return jsonify({"name": "Khabir V2 API", "version": "2.0.0"})

    return app


app = create_app()

