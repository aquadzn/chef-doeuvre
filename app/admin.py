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
from .models import User, File


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
        users = User.query.all()
        files = File.query.all()

        return render_template("admin/dashboard.html", users=users, files=files)


@admin.route("/admin/dashboard/delete_user/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):

    if current_user.id != 1:
        return render_template("404.html"), 404
    else:
        User.query.filter_by(id=user_id).delete()
        db.session.commit()

        logging.info(f"admin - utilisateur #{user_id} supprimé.")
        flash("Utilisateur supprimée.")
        return redirect(url_for("admin.dashboard"))


@admin.route("/admin/dashboard/delete_file/<int:file_id>", methods=["POST"])
@login_required
def delete_file(file_id):

    if current_user.id != 1:
        return render_template("404.html"), 404
    else:
        filepath = os.path.join(
            "app/static/uploads", File.query.filter_by(id=file_id).first().filename
        )
        if os.path.exists(filepath):
            os.remove(filepath)
            logging.info(f"admin - {filepath} supprimé.")

        File.query.filter_by(id=file_id).delete()
        db.session.commit()

        logging.info("admin - record SQL #{file_id} supprimé.")
        flash("Image supprimée.")
        return redirect(url_for("admin.dashboard"))
