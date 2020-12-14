import logging
from datetime import datetime
from tempfile import NamedTemporaryFile

import config

import requests as r

from google.cloud import storage
from google.cloud.exceptions import NotFound

from flask import Flask, flash, redirect, request, url_for, render_template, send_file

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
from werkzeug.security import generate_password_hash, check_password_hash


TRAD_LABELS = {
    "apple_pie": "Tarte aux pommes",
    "baby_back_ribs": "Côtes levées de porc",
    "baklava": "Baklava",
    "beef_carpaccio": "Carpaccio de boeuf",
    "beef_tartare": "Tartare de boeuf",
    "beet_salad": "Salade de betteraves",
    "beignets": "Beignets",
    "bibimbap": "Bibimbap",
    "bread_pudding": "Pouding au pain",
    "breakfast_burrito": "Petit déjeuner burrito",
    "bruschetta": "Bruschetta",
    "caesar_salad": "Salade César",
    "cannoli": "Cannoli",
    "caprese_salad": "Salade Caprese",
    "carrot_cake": "Gâteau à la carotte",
    "ceviche": "Ceviche",
    "cheesecake": "Cheesecake",
    "cheese_plate": "Assiette de fromage",
    "chicken_curry": "Poulet au curry",
    "chicken_quesadilla": "Quesadilla de poulet",
    "chicken_wings": "Ailes de poulet",
    "chocolate_cake": "Gateau au chocolat",
    "chocolate_mousse": "Mousse au chocolat",
    "churros": "Churros",
    "clam_chowder": "Chaudrée de palourdes",
    "club_sandwich": "Club sandwich",
    "crab_cakes": "Beignets de crabe",
    "creme_brulee": "Crème brulée",
    "croque_madame": "Croque Madame",
    "cup_cakes": "Cupcakes",
    "deviled_eggs": "Oeufs farcis",
    "donuts": "Donuts",
    "dumplings": "Dumplings",
    "edamame": "Edamame",
    "eggs_benedict": "Oeufs Bénédicte",
    "escargots": "Escargots",
    "falafel": "Falafel",
    "filet_mignon": "Filet mignon",
    "fish_and_chips": "Poisson et frites",
    "foie_gras": "Foie gras",
    "french_fries": "Frites",
    "french_onion_soup": "Soupe à l'oignon française",
    "french_toast": "Pain perdu",
    "fried_calamari": "Calmars frits",
    "fried_rice": "Riz sauté",
    "frozen_yogurt": "Yaourt glacé",
    "garlic_bread": "Pain à l'ail",
    "gnocchi": "Gnocchi",
    "greek_salad": "Salade grecque",
    "grilled_cheese_sandwich": "Sandwich au fromage fondu",
    "grilled_salmon": "Saumon grillé",
    "guacamole": "Guacamole",
    "gyoza": "Gyoza",
    "hamburger": "Hamburger",
    "hot_and_sour_soup": "Soupe aigre-douce",
    "hot_dog": "Hot-dog",
    "huevos_rancheros": "Huevos rancheros",
    "hummus": "Hoummous",
    "ice_cream": "Crème glacée",
    "lasagna": "Lasagne",
    "lobster_bisque": "Bisque de homard",
    "lobster_roll_sandwich": "Sandwich roulé au homard",
    "macaroni_and_cheese": "Macaroni au fromage",
    "macarons": "Macarons",
    "miso_soup": "Soupe miso",
    "mussels": "Moules",
    "nachos": "Nachos",
    "omelette": "Omelette",
    "onion_rings": "Rondelles d'oignon",
    "oysters": "Huîtres",
    "pad_thai": "Pad thaï",
    "paella": "Paëlla",
    "pancakes": "Crêpes",
    "panna_cotta": "Panna cotta",
    "peking_duck": "Canard laqué",
    "pho": "Pho",
    "pizza": "Pizza",
    "pork_chop": "Côtelette de porc",
    "poutine": "Poutine",
    "prime_rib": "Côte de boeuf",
    "pulled_pork_sandwich": "Sandwich au porc effiloché",
    "ramen": "Ramen",
    "ravioli": "Ravioli",
    "red_velvet_cake": "Gâteau Red Velvet",
    "risotto": "Risotto",
    "samosa": "Samosa",
    "sashimi": "Sashimi",
    "scallops": "Coquilles Saint-Jacques",
    "seaweed_salad": "Salade d'algues",
    "shrimp_and_grits": "Crevettes et gruau",
    "spaghetti_bolognese": "Spaghetti bolognaise",
    "spaghetti_carbonara": "Spaghetti carbonara",
    "spring_rolls": "Rouleaux de printemps",
    "steak": "Steak",
    "strawberry_shortcake": "Tarte sablée à la fraise",
    "sushi": "Sushi",
    "tacos": "Tacos",
    "takoyaki": "Takoyaki",
    "tiramisu": "Tiramisu",
    "tuna_tartare": "Tartare de thon",
    "waffles": "Gaufres",
}


app = Flask(__name__)


def upload_blob(source, destination_blob_name):

    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(source.read(), content_type=source.content_type)

    # print(f"File {source_file_name} uploaded to {destination_blob_name}.")


def download_blob(source_blob_name):

    blob = bucket.get_blob(source_blob_name)

    return blob.download_as_bytes()

    # print(f"Blob {source_blob_name} downloaded to {destination_file_name}.")


def delete_blob(blob_name):

    try:
        bucket.delete_blob(blob_name)
        print(f"Blob {blob_name} deleted.")
    except NotFound:
        pass


def page_not_found(e):
    return render_template("errors/404.html"), 404


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
app.config["SQLALCHEMY_DATABASE_URI"] = config.POSTGRE_URI
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
    label = db.Column(db.String(200))
    confidence = db.Column(db.Float)
    uploaded_at = db.Column(db.DateTime)


login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    return render_template("errors/401.html"), 401


storage_client = storage.Client.from_service_account_json("gcp-credentials.json")
bucket = storage_client.bucket("uploads-chef-oeuvre")


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

    username = request.form.get("username").lower()
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password) or user.id == 1:
        logging.error(f"{username} - tentative de connexion échouée")
        flash("Adresse mail ou mot de passe incorrecte. Veuillez réessayez.")
        return redirect(url_for("login"))

    login_user(user, remember=remember)

    logging.info(f"{username} - connexion réussie")
    return redirect(url_for("account"))


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup_post():

    username = request.form.get("username").lower()
    email = request.form.get("email").lower()
    password = request.form.get("password")

    user_name = User.query.filter_by(username=username).first()
    user_mail = User.query.filter_by(email=email).first()

    if user_name is None and user_mail is None:
        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password, method="sha256"),
            created_at=datetime.now(),
        )

        db.session.add(new_user)
        db.session.commit()

        logging.info(f"{username} - création de compte")
        return redirect(url_for("login"))
    else:
        logging.error(f"{username} - {email} déjà associé à un compte.")
        flash("Un compte est déjà associé à cette adresse mail.")
        return redirect(url_for("signup"))


@app.route("/logout")
@login_required
def logout():
    logging.info(f"{current_user.username} - déconnexion")
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

    username = request.form.get("username").lower()
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password) or user.id != 1:
        logging.error(f"{username} - ATTENTION TENTATIVE DE CONNEXION ADMIN")
        flash("Vous n'avez pas accès à cette partie du site.")
        return redirect(url_for("login"))  # auth.admin_login

    login_user(user)

    logging.info(f"{username} - connexion réussie")
    return redirect(url_for("admin_index"))


@app.route("/admin")
@login_required
def admin_index():
    if current_user.id != 1:
        return render_template("errors/404.html"), 404
    else:
        return render_template("admin/index.html")


@app.route("/admin/dashboard")
@login_required
def admin_dashboard():

    if current_user.id != 1:
        return render_template("errors/404.html"), 404
    else:
        users = User.query.all()
        files = File.query.all()

        return render_template("admin/dashboard.html", users=users, files=files)


@app.route("/admin/dashboard/delete_user/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):

    if current_user.id != 1:
        return render_template("errors/404.html"), 404
    else:
        User.query.filter_by(id=user_id).delete()
        db.session.commit()

        logging.info(f"admin - utilisateur #{user_id} supprimé.")
        flash("Utilisateur supprimée.")
        return redirect(url_for("admin_dashboard"))


@app.route("/admin/dashboard/delete_file/<int:file_id>", methods=["POST"])
@login_required
def delete_file(file_id):

    if current_user.id != 1:
        return render_template("errors/404.html"), 404
    else:
        file_row = File.query.filter_by(id=file_id).first()

        delete_blob(f"{file_row.username}/{file_row.filename}")
        logging.info(f"admin - {file_row.username}/{file_row.filename} supprimé.")

        File.query.filter_by(id=file_id).delete()
        db.session.commit()

        logging.info("admin - record SQL #{file_id} supprimé.")
        flash("Image supprimée.")
        return redirect(url_for("admin_dashboard"))


# ------------------- ACTIONS -------------------


@app.route("/account")
@login_required
def account():

    logging.info(f"{current_user.username} - accès à son compte")
    return render_template(
        "account.html", username=current_user.username, email=current_user.email
    )


@app.route("/account/delete/images")
@login_required
def delete_all():

    blobs = storage_client.list_blobs(
        bucket_or_name="uploads-chef-oeuvre", prefix=f"{current_user.username}/"
    )
    for b in blobs:
        b.delete()

    # bucket.delete_blobs(blobs=bucket.list_blobs(prefix=folder))

    File.query.filter_by(username=current_user.username).delete()
    db.session.commit()

    logging.info(f"{current_user.username} - tous les record SQL supprimés.")
    flash("Toutes vos images ont été supprimées.", "success")
    return redirect(url_for("account"))


@app.route("/account/delete/account")
@login_required
def delete_account():

    blobs = storage_client.list_blobs(
        bucket_or_name="uploads-chef-oeuvre", prefix=f"{current_user.username}/"
    )
    for b in blobs:
        b.delete()

    File.query.filter_by(username=current_user.username).delete()
    User.query.filter_by(username=current_user.username).delete()

    logout_user()
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/images")
@login_required
def images():

    logging.info(f"{current_user.username} - accès à ses images")
    files = File.query.filter_by(username=current_user.username).all()

    return render_template("images.html", files=files)


@app.route("/images/download/<string:filename>")
@login_required
def download(filename):

    blob = bucket.get_blob(f"{current_user.username}/{filename}")
    # url = blob.generate_signed_url(expiration=10, version='v4')

    with NamedTemporaryFile() as file_obj:
        blob.download_to_filename(file_obj.name)

        return send_file(file_obj.name, attachment_filename=filename)


@app.route("/images/delete/<int:post_id>")
@login_required
def delete(post_id):

    delete_blob(
        f"{current_user.username}/{File.query.filter_by(id=post_id).first().filename}"
    )
    logging.info(f"{current_user.username} - image {post_id} supprimé.")

    File.query.filter_by(id=post_id).delete()
    db.session.commit()

    logging.info(f"{current_user.username} - record SQL #{post_id} supprimé.")
    flash("Image supprimée.")
    return redirect(url_for("images"))


@app.route("/analysis")
@login_required
def analysis():
    labels = (
        db.session.query(File.label).filter_by(username=current_user.username).all()
    )
    preds = (
        db.session.query(File.confidence)
        .filter_by(username=current_user.username)
        .all()
    )

    logging.info(f"{current_user.username} - accès à ses analyses")
    return render_template(
        "analysis.html", username=current_user.username, labels=labels, preds=preds
    )


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():

    if request.method == "POST":

        if "image" not in request.files:
            logging.error(f"{current_user.username} - erreur d'envoi de fichier")
            flash("Pas de fichier!", "error")
            return redirect(url_for("upload"))

        file = request.files.get("image")

        if file.filename == "":
            logging.error(f"{current_user.username} - erreur nom de fichier")
            flash("Pas de fichier!", "error")
            return redirect(url_for("upload"))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            upload_blob(
                source=file,
                destination_blob_name=f"{current_user.username}/{filename}",
            )
            logging.info(f"{current_user.username} - {filename} sauvegardé")

            file.seek(0)
            response = r.post(
                url=config.CLOUD_FUNCTION_URL,  # URL Cloud Functions
                headers={"Content-Type": "application/octet-stream"},
                data=file.stream,
            ).json()

            label = TRAD_LABELS[response["label"]]
            confidence = response["confidence"]

            # Cas où la prédiction est incertaine selon un taux purement arbitraire
            if confidence < 50.0:
                label = f"Incertain - {label}"

            new_file = File(
                username=current_user.username,
                filename=file.filename,
                label=label,
                confidence=confidence,
                uploaded_at=datetime.now(),
            )

            db.session.add(new_file)
            db.session.commit()

            logging.info(f"{current_user.username} - record SQL ajouté")
            # flash("Fichier envoyé!", "success")
            flash(f"Détecté: {label} ({confidence}%)", "success")
            return redirect(request.url)

    return render_template("upload.html", username=current_user.username)
