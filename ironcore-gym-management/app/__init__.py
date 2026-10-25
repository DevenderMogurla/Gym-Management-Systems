import sqlite3
from flask import Flask, g
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from .routes import bp
    app.register_blueprint(bp)

    with app.app_context():
        from .db import init_db
        init_db()

    return app
