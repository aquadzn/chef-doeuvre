# Chef d'oeuvre

---

## Installation

### Makefile references

```bash
Usage:
  make 

Utility
  help                      Display help
  setup                     Install Python requirements
  lint                      Lint Python files and check for potential security issues.
  test                      Run Python tests (no warnings)
  run                       Run local Flask app
  build_docker              Build local Docker image
  deploy_cloud_functions    Deploy AI function to Google Cloud Functions
  get_cloud_functions_url   Grab Google Cloud Functions URL
  deploy_cloud_image        Deploy app image to Google Container Registry
  deploy_cloud_run          Deploy app to Google Cloud Run
  delete_cloud_run          Delete Cloud Run service
  delete_cloud_functions    Delete Cloud Functions
  delete_cloud_image        Delete image on Google Container Registry
  delete_all                Delete all Google stuff
  create_bucket             Create a Google Storage Bucket
  clean_bucket              Clean a Google Storage Bucket
```


### Setup

Create a config.py with this structure:

```python
import os


FLASK_KEY = os.urandom(32)
JSON_GCP = "./gcp-credentials.json"
CLOUD_FUNCTION_URL = "cloud_function_url"

POSTGRE_URI = "postgres://your_url"

ADMIN_MAIL = "mail"
ADMIN_USERNAME = "admin"
ADMIN_PWD = "admin"
```

then

```bash
# Install local dependencies
make setup

# Run Python tests
make test

# Lint, format and check for security issues in Python files. Also remove cache folders
make lint

# Run Flask app locally (opt args: HOST, PORT)
make run

# Build image with Docker locally
make build_docker
```

### Deployment (in order)

```bash
# Deploy to GCP Cloud Functions
make deploy_cloud_functions FUNCTION_NAME=model-chef-oeuvre
```

**Grab the URL** of the function using `make get_cloud_functions_url` and assign it to **CLOUD_FUNCTION_URL** in *config.py* line 6.

```bash
# Deploy image to GCR
make deploy_cloud_image IMAGE_NAME=image-chef-oeuvre

# Deploy to GCP Cloud Run
make deploy_cloud_run CLOUD_RUN_NAME=app-chef-oeuvre IMAGE_NAME=image-chef-oeuvre

```

**Grab the URL** and you're done!


### Utils

```bash
# Delete Cloud Run
make delete_cloud_run CLOUD_RUN_NAME=app-chef-oeuvre

# Delete Cloud Functions
make delete_cloud_functions FUNCTION_NAME=model-chef-oeuvre

# Delete image from gcr.io
make delete_cloud_image IMAGE_NAME=image-chef-oeuvre

# Delete Function, Run and Image
make delete_all

# Create a GCP Bucket with name
make create_bucket BUCKET_NAME=uploads

# Remove all files in a GCP Bucket
make clean_bucket BUCKET_NAME=uploads
```