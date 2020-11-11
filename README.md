# Chef d'oeuvre


```bash
# Install local dependencies
make setup

# Lint Python files and remove cache folders
make lint

# Run Python tests
make test

# Run Flask app locally (opt args: HOST, PORT)
make run

# Build image with Docker locally
make build_docker

# Deploy to GCP Cloud Run
make deploy_gcp

# Create GCP Bucket with name
make create_bucket BUCKET_NAME=uploads

# Clean GCP Bucket
make clean_bucket BUCKET_NAME=uploads
```
