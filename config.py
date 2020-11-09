import os


FLASK_KEY = os.urandom(32)
FLASK_DB = "sqlite:///db.sqlite" # os.environ.get("FLASK_DB")
FLASK_UPLOAD = "app/static/uploads/"

# S3_BUCKET = os.environ.get("S3_BUCKET_NAME")
# S3_KEY = os.environ.get("S3_ACCESS_KEY")
# S3_SECRET = os.environ.get("S3_SECRET_ACCESS_KEY")
# S3_LOCATION = f"http://{S3_BUCKET}.s3.amazonaws.com/"
