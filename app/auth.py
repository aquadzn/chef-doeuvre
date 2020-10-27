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
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

from . import db
from .models import User


auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def login_post():

    username = request.form.get("username")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        logging.error(f"{user} - tentative de connexion échouée")
        flash("Adresse mail ou mot de passe incorrecte. Veuillez réessayez.")
        return redirect(url_for("auth.login"))

    login_user(user, remember=remember)

    logging.info(f"{username} - connexion réussie")
    return redirect(url_for("main.profile"))


@auth.route("/signup")
def signup():
    return render_template("signup.html")


@auth.route("/signup", methods=["POST"])
def signup_post():

    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if user:
        logging.error(f"{username} - {email} déjà associé à un compte.")
        flash("Un compte est déjà associé à cette adresse mail.")
        return redirect(url_for("auth.signup"))

    new_user = User(
        username=username,
        email=email,
        password=generate_password_hash(password, method="sha256"),
    )

    db.session.add(new_user)
    db.session.commit()

    logging.info(f"{username} - création de compte")
    return redirect(url_for("auth.login"))


@auth.route("/logout")
@login_required
def logout():
    logging.info(f"{current_user.username} - déconnexion")
    logout_user()
    return redirect(url_for("main.index"))
