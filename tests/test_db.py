import os
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash


app = Flask("test")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test_db.sqlite"
db = SQLAlchemy(app)


class User(db.Model):
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
    uploaded_at = db.Column(db.DateTime)


def build_db():
    try:
        db.drop_all()
        db.create_all()
        db.session.commit()
        return True
    except SQLAlchemyError:
        return False


def add_user():
    try:
        test_user = User(
            username="test",
            email="test@mail.com",
            password=generate_password_hash("azerty", method="sha256"),
            created_at=datetime.now(),
        )

        db.session.add(test_user)
        db.session.commit()
        return True
    except SQLAlchemyError:
        return False


def add_file():
    try:
        test_file = File(
            username="test",
            filename="test.jpg",
            label="test_label",
            uploaded_at=datetime.now(),
        )

        db.session.add(test_file)
        db.session.commit()
        return True
    except SQLAlchemyError:
        return False


def query_user():
    try:
        test_user = User.query.filter_by(username="test").first()
        assert isinstance(test_user, User)
        return True
    except SQLAlchemyError:
        return False


def query_file():
    try:
        test_file = File.query.filter_by(filename="test.jpg").first()
        assert isinstance(test_file, File)
        return True
    except SQLAlchemyError:

        return False


def delete_user():
    try:
        User.query.filter_by(username="test").delete()
        db.session.commit()
        assert User.query.filter_by(username="test") is None
        return True
    except SQLAlchemyError:
        return False


def delete_file():
    try:
        File.query.filter_by(filename="test.jpg").delete()
        db.session.commit()
        assert File.query.filter_by(filename="test.jpg") is None
        return True
    except SQLAlchemyError:
        return False


def delete_db():
    try:
        os.remove("/tmp/test_db.sqlite")
        assert not os.path.exists("/tmp/test_db.sqlite")
        return True
    except SQLAlchemyError:
        return False


def test_build_db():
    assert build_db()


def test_add_user():
    assert add_user()


def test_add_file():
    assert add_file()


def test_query_user():
    assert query_user()


def test_query_file():
    assert query_file()
