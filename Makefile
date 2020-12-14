HOST=0.0.0.0
PORT=8080
BUCKET_NAME=uploads-chef-oeuvre
CLOUD_RUN_NAME=app-chef-oeuvre
IMAGE_NAME=image-chef-oeuvre
FUNCTION_NAME=model-chef-oeuvre
REGION=us-east1


##@ Utility
help:  ## Display help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)


setup:	## Install Python requirements
	pip install -r requirements.txt


lint:	## Lint Python files and check for potential security issues.
	black *.py
	black */*.py
	flake8 --max-line-length=88 *.py
	flake8 --max-line-length=88 */*.py
	bandit *.py
	rm -rf __pycache__
	rm -rf */__pycache__
	rm -rf .pytest_cache


test:	## Run Python tests (no warnings)
	pytest --disable-warnings


run:	## Run local Flask app
	python main.py --host $(HOST) --port $(PORT)


build_docker:	## Build local Docker image
	docker build -t chef-oeuvre .


deploy_cloud_functions:	## Deploy AI function to Google Cloud Functions
	gcloud functions deploy $(FUNCTION_NAME) \
		--source=cloud_functions/ \
		--entry-point=run \
		--runtime=python38 \
		--memory=1024MB \
		--timeout=60 \
		--trigger-http \
		--region=$(REGION) \
		--allow-unauthenticated


get_cloud_functions_url:	## Grab Google Cloud Functions URL
	gcloud functions describe $(FUNCTION_NAME) --region $(REGION) | grep -o 'https://.*$(FUNCTION_NAME)'


deploy_cloud_image:	## Deploy app image to Google Container Registry
	gcloud builds submit --tag gcr.io/ml-dl-77/$(IMAGE_NAME)


deploy_cloud_run:	## Deploy app to Google Cloud Run
	gcloud run deploy $(CLOUD_RUN_NAME) \
		--image gcr.io/ml-dl-77/$(IMAGE_NAME) \
		--platform=managed \
		--allow-unauthenticated \
		--region=$(REGION) \
		--concurrency=1 \
		--memory=2Gi


delete_cloud_run:	## Delete Cloud Run service
	gcloud run services delete $(CLOUD_RUN_NAME) --platform=managed --region=$(REGION)


delete_cloud_functions:	## Delete Cloud Functions
	gcloud functions delete $(FUNCTION_NAME) --region=$(REGION)


delete_cloud_image:	## Delete image on Google Container Registry
	gcloud container images delete --force-delete-tags gcr.io/ml-dl-77/$(IMAGE_NAME)


delete_all:	## Delete all Google stuff
	gcloud run services delete $(CLOUD_RUN_NAME) --platform=managed --region=$(REGION)
	gcloud functions delete $(FUNCTION_NAME) --region=$(REGION)
	gcloud container images delete --force-delete-tags gcr.io/ml-dl-77/$(IMAGE_NAME)


create_bucket:	## Create a Google Storage Bucket
	gsutil mb gs://$(BUCKET_NAME)


clean_bucket:	## Clean a Google Storage Bucket
	gsutil -m rm -r gs://$(BUCKET_NAME)/*
