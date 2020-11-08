import os
import logging

from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

# Disable Flask useless logging stuff
logger = logging.getLogger("werkzeug")
logger.setLevel(logging.ERROR)

# Set our logger
logging.basicConfig(
    format="%(asctime)s | [%(levelname)s] | %(message)s",
    datefmt="%d/%m/%Y %I:%M:%S",
    level=logging.DEBUG,
    handlers=[logging.FileHandler("app/debug.log"), logging.StreamHandler()],
)


def create_app():

    app = Flask(__name__)

    from .config import FLASK_KEY, FLASK_DB, FLASK_UPLOAD

    app.config["SECRET_KEY"] = config.FLASK_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = config.FLASK_DB
    app.config["UPLOAD_FOLDER"] = config.FLASK_UPLOAD
    app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def page_not_found(e):
        return render_template("404.html"), 404

    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from .admin import admin as admin_blueprint

    app.register_blueprint(admin_blueprint)

    app.register_error_handler(404, page_not_found)

    return app
