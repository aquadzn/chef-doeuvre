import os
import logging

from flask import (
    Blueprint,
    render_template,
    current_app,
    redirect,
    request,
    url_for,
    flash,
)
from flask_login import login_required, current_user

from . import db
from .models import File


admin = Blueprint("admin", __name__)


@admin.route("/admin")
@login_required
def index():
    if current_user.id != 1:
        return render_template("404.html"), 404
    else:
        return render_template("admin/index.html")


@admin.route("/admin/dashboard")
@login_required
def dashboard():
    if current_user.id != 1:
        return render_template("404.html"), 404
    else:
        return render_template("admin/dashboard.html")
