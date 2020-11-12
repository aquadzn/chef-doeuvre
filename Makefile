HOST=0.0.0.0
PORT=8080
BUCKET_NAME=uploads-chef-oeuvre
CLOUD_RUN_NAME=app-chef-oeuvre
IMAGE_NAME=image-chef-oeuvre
FUNCTION_NAME=model-chef-oeuvre

setup:
	pip install -r requirements.txt


lint:
	black *.py
	black */*.py
	flake8 --max-line-length=88 *.py
	flake8 --max-line-length=88 */*.py
	bandit *.py
	rm -rf __pycache__
	rm -rf */__pycache__
	rm -rf .pytest_cache


test:
	pytest --disable-warnings


run:
	python main.py --host $(HOST) --port $(PORT)


build_docker:
	docker build -t chef-oeuvre .


deploy_cloud_functions:
	gcloud functions deploy $(FUNCTION_NAME) \
		--source=cloud_functions/ \
		--entry-point=run \
		--runtime=python38 \
		--memory=1024MB \
		--trigger-http \
		--region=us-east1 \
		--allow-unauthenticated


deploy_cloud_image:
	gcloud builds submit --tag gcr.io/ml-dl-77/$(IMAGE_NAME)


deploy_cloud_run:
	gcloud run deploy $(CLOUD_RUN_NAME) \
		--image gcr.io/ml-dl-77/$(IMAGE_NAME) \
		--platform=managed \
		--allow-unauthenticated \
		--region=us-east1 \
		--concurrency=1 \
		--memory=2Gi


delete_cloud_run:
	gcloud run services delete $(CLOUD_RUN_NAME) --platform=managed --region=us-east1


delete_cloud_functions:
	gcloud run services delete $(FUNCTION_NAME) --platform=managed --region=us-east1


delete_cloud_image:
	gcloud container images delete --force-delete-tags gcr.io/ml-dl-77/$(IMAGE_NAME)


create_bucket:
	gsutil mb gs://$(BUCKET_NAME)


clean_bucket:
	gsutil -m rm -r gs://$(BUCKET_NAME)/*
