# Chef d'oeuvre


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

# Deploy to GCP Cloud Run
make deploy_gcp IMAGE_NAME=chef-oeuvre SERVICE_NAME=chef-oeuvre

# Delete Cloud Run service
make delete_service SERVICE_NAME=chef-oeuvre

# Delete image from gcr.io
make delete_image IMAGE_NAME=chef-oeuvre

# Create GCP Bucket with name
make create_bucket BUCKET_NAME=uploads

# Clean GCP Bucket
make clean_bucket BUCKET_NAME=uploads
```
