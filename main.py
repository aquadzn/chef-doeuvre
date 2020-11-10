import os
import string
import random
import argparse

# import logging
from datetime import datetime

import config

from fastai.vision.all import load_learner

from flask import Flask, flash, redirect, request, url_for, render_template

from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    UserMixin,
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)

from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)


def get_args():
    parser = argparse.ArgumentParser(description="Run Flask web server")
    parser.add_argument("--host", type=str, help="Hostname (default: 127.0.0.1")
    parser.add_argument("--port", type=int, help="Port (default: 5000")

    args = parser.parse_args()
    return args


def page_not_found(e):
    return render_template("404.html"), 404


def file_too_large(e):
    flash("Le fichier excède 2MB!", "error")
    return redirect(url_for("upload")), 413


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in [
        "png",
        "jpg",
        "jpeg",
    ]


app.config["SECRET_KEY"] = config.FLASK_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = config.FLASK_DB
app.config["UPLOAD_FOLDER"] = config.FLASK_UPLOAD
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

app.register_error_handler(404, page_not_found)
app.register_error_handler(413, file_too_large)

db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(100))
    created_at = db.Column(db.DateTime)


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    filename = db.Column(db.String(200))
    uploaded_at = db.Column(db.DateTime)


login_manager = LoginManager()
# login_manager.login_view = "auth.login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def build_sample_db():

    db.drop_all()
    db.create_all()

    admin_user = User(
        username="admin",
        email="admin@mail.com",
        password=generate_password_hash("admin", method="sha256"),
        created_at=datetime.now(),
    )
    db.session.add(admin_user)

    usernames = [
        "jean",
        "william",
        "sylvere",
    ]

    for i in range(len(usernames)):
        test_user = User(
            username=usernames[i],
            email=f"{usernames[i]}@mail.com",
            password=generate_password_hash("azerty", method="sha256"),
            created_at=datetime.now(),
        )
        print(f"Utilisateur '{usernames[i]}' crée.")
        print("Mot de passe: azerty")
        db.session.add(test_user)

    db.session.commit()
    return


# ------------------- MAIN -------------------


@app.route("/")
def index():
    return render_template("index.html")


# ------------------- AUTH -------------------


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():

    username = request.form.get("username")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password) or user.id == 1:
        # logging.error(f"{username} - tentative de connexion échouée")
        flash("Adresse mail ou mot de passe incorrecte. Veuillez réessayez.")
        return redirect(url_for("login"))

    login_user(user, remember=remember)

    # logging.info(f"{username} - connexion réussie")
    return redirect(url_for("profile"))


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup_post():

    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if user:
        # logging.error(f"{username} - {email} déjà associé à un compte.")
        flash("Un compte est déjà associé à cette adresse mail.")
        return redirect(url_for("signup"))

    new_user = User(
        username=username,
        email=email,
        password=generate_password_hash(password, method="sha256"),
        created_at=datetime.now(),
    )

    db.session.add(new_user)
    db.session.commit()

    # logging.info(f"{username} - création de compte")
    return redirect(url_for("login"))


@app.route("/logout")
@login_required
def logout():
    # logging.info(f"{current_user.username} - déconnexion")
    logout_user()
    return redirect(url_for("index"))


# ------------------- ADMIN -------------------


@app.route("/admin/login")
def admin_login():
    return render_template("admin/login.html")


@app.route("/admin/login", methods=["POST"])
def admin_login_post():

    if current_user.is_authenticated:
        logout_user()

    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password) or user.id != 1:
        # # logging.error(f"{username} - tentative de connexion échouée")
        flash("Vous n'avez pas accès à cette partie du site.")
        return redirect(url_for("login"))  # auth.admin_login

    login_user(user)

    # # logging.info(f"{username} - connexion réussie")
    return redirect(url_for("admin_index"))


@app.route("/admin")
@login_required
def admin_index():
    if current_user.id != 1:
        return render_template("404.html"), 404
    else:
        return render_template("admin/index.html")


@app.route("/admin/dashboard")
@login_required
def admin_dashboard():

    if current_user.id != 1:
        return render_template("404.html"), 404
    else:
        users = User.query.all()
        files = File.query.all()

        return render_template("admin/dashboard.html", users=users, files=files)


@app.route("/admin/dashboard/delete_user/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):

    if current_user.id != 1:
        return render_template("404.html"), 404
    else:
        User.query.filter_by(id=user_id).delete()
        db.session.commit()

        # logging.info(f"admin - utilisateur #{user_id} supprimé.")
        flash("Utilisateur supprimée.")
        return redirect(url_for("admin_dashboard"))


@app.route("/admin/dashboard/delete_file/<int:file_id>", methods=["POST"])
@login_required
def delete_file(file_id):

    if current_user.id != 1:
        return render_template("404.html"), 404
    else:
        filepath = os.path.join(
            "/mnt/images/", File.query.filter_by(id=file_id).first().filename
        )
        if os.path.exists(filepath):
            os.remove(filepath)
            # logging.info(f"admin - {filepath} supprimé.")

        File.query.filter_by(id=file_id).delete()
        db.session.commit()

        # logging.info("admin - record SQL #{file_id} supprimé.")
        flash("Image supprimée.")
        return redirect(url_for("admin_dashboard"))


# ------------------- ACTIONS -------------------


@app.route("/profile")
@login_required
def profile():

    # logging.info(f"{current_user.username} - accès à son profil")
    return render_template(
        "profile.html", username=current_user.username, email=current_user.email
    )


@app.route("/images")
@login_required
def images():

    # logging.info(f"{current_user.username} - accès à ses images")
    files = File.query.filter_by(username=current_user.username).all()

    return render_template("images.html", files=files)


@app.route("/images/delete/<int:post_id>", methods=["POST"])
@login_required
def delete(post_id):

    filepath = os.path.join(
        "/mnt/images/", File.query.filter_by(id=post_id).first().filename
    )
    if os.path.exists(filepath):
        os.remove(filepath)
        # logging.info(f"{current_user.username} - {filepath} supprimé.")

    File.query.filter_by(id=post_id).delete()
    db.session.commit()

    # logging.info(f"{current_user.username} - record SQL #{post_id} supprimé.")
    flash("Image supprimée.")
    return redirect(url_for("images"))


@app.route("/analysis")
@login_required
def analysis():

    # logging.info(f"{current_user.username} - accès à ses analyses")
    return render_template("analysis.html", username=current_user.username)


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():

    if request.method == "POST":

        if "file" not in request.files:
            # logging.error(f"{current_user.username} - erreur d'envoi de fichier")
            flash("Pas de fichier!", "error")
            return redirect(url_for("upload"))

        file = request.files["file"]

        if file.filename == "":
            # logging.error(f"{current_user.username} - erreur d'envoi de fichier")
            flash("Pas de fichier!", "error")
            return redirect(url_for("upload"))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join("/mnt/images/", filename))
            # logging.info(f"{current_user.username} - {filename} sauvegardé")

            new_file = File(
                username=current_user.username,
                filename=file.filename,
                uploaded_at=datetime.now(),
            )

            label, label_idx, _ = learner.predict(
                os.path.join("/mnt/images/", filename)
            )

            db.session.add(new_file)
            db.session.commit()

            # logging.info(f"{current_user.username} - record SQL ajouté")
            # flash("Fichier envoyé!", "success")
            flash(f"Label: {str(label)} ({int(label_idx)})", "success")
            return redirect(request.url)

    return render_template("upload.html", username=current_user.username)


if __name__ == "__main__":

    if not os.path.exists("db.sqlite"):
        build_sample_db()
    else:
        os.remove("db.sqlite")
        print("Le fichier 'db.sqlite' a été supprimé.")
        build_sample_db()

    learner = load_learner("model.pkl", cpu=True)
    args = get_args()

    app.run(host=args.host, port=args.port, debug=False)
