import os
from datetime import datetime

from sqlalchemy import exc
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from . import db
from .models import File


main = Blueprint("main", __name__)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in [
        "png",
        "jpg",
        "jpeg",
    ]


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/profile")
@login_required
def profile():
    return render_template(
        "profile.html", username=current_user.username, email=current_user.email
    )


@main.route("/images")
@login_required
def images():

    files = File.query.filter_by(username=current_user.username).all()

    return render_template("images.html", files=files)


@main.route("/images/delete/<int:post_id>", methods=["POST"])
@login_required
def delete(post_id):

    filepath = os.path.join("app/static/uploads", File.query.filter_by(id=post_id).first().filename)
    if os.path.exists(filepath):
        os.remove(filepath)

    File.query.filter_by(id=post_id).delete()
    db.session.commit()

    flash("Image supprimée.")
    return redirect(url_for("main.images"))


@main.route("/upload", methods=["GET", "POST"])
@login_required
def upload():

    if request.method == "POST":

        if "file" not in request.files:
            flash("Pas de fichier!", "error")
            return redirect(url_for("main.upload"))

        file = request.files["file"]

        if file.filename == "":
            flash("Pas de fichier!", "error")
            return redirect(url_for("main.upload"))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join("app/static/uploads/", filename))

            new_file = File(
                username=current_user.username,
                filename=file.filename,
                date=datetime.now(),
            )

            db.session.add(new_file)
            db.session.commit()

            flash("Fichier envoyé!", "success")
            return redirect(request.url)

    return render_template("upload.html", username=current_user.username)
