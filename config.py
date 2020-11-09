import os


FLASK_KEY = os.urandom(32)
FLASK_DB = "sqlite:///db.sqlite"
FLASK_UPLOAD = "/mnt/images/uploads/"

# S3_BUCKET = os.environ.get("S3_BUCKET_NAME")
# S3_KEY = os.environ.get("S3_ACCESS_KEY")
# S3_SECRET = os.environ.get("S3_SECRET_ACCESS_KEY")
# S3_LOCATION = f"http://{S3_BUCKET}.s3.amazonaws.com/"
