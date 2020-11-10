import os


FLASK_KEY = os.urandom(32)
FLASK_DB = "sqlite:///db.sqlite"
FLASK_UPLOAD = "./static/uploads/"
JSON_GCP = "./gcp-credentials.json"
