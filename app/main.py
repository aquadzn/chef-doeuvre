import os

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename


main = Blueprint("main", __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ["png", "jpg", "jpeg"]


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html", name=current_user.name, email=current_user.email)


@main.route("/upload", methods=["GET", "POST"])
@login_required
def upload():

    if request.method == 'POST':

        if 'file' not in request.files:
            flash("Pas de fichier!", "error")
            return redirect(url_for("main.upload"))

        file = request.files['file']

        if file.filename == "":
            flash("Pas de fichier!", "error")
            return redirect(url_for("main.upload"))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(os.path.abspath("app/uploads/"), filename))

            flash("Fichier envoyé!", "success")
            return redirect(request.url)

    return render_template("upload.html", name=current_user.name)
