from flask_login import UserMixin

from . import db


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(500), unique=True)
    password = db.Column(db.String(100))


class Upload(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200))
    date = db.Column(db.DateTime)
