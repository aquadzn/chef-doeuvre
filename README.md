# Chef d'oeuvre

---

### Setup:

```bash
# Install local dependencies
make setup

# Lint, format and check for security issues in Python files. Also remove cache folders
make lint

# Run Python tests
make test

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

**Grab the URL** of the function and place it in the *url* parameter for the POST request in `main_gcp.py` arround line 408

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