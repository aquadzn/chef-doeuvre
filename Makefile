HOST=0.0.0.0
PORT=8080
BUCKET_NAME=chef-oeuvre


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


deploy_gcp:
	gcloud builds submit --tag gcr.io/ml-dl-77/chef-oeuvre
	gcloud run deploy chef-oeuvre \
		--image gcr.io/ml-dl-77/chef-oeuvre \
		--platform=managed \
		--allow-unauthenticated \
		--region=us-east1 \
		--concurrency=1 \
		--memory=2Gi


delete_gcp:
	gcloud container images delete --force-delete-tags gcr.io/ml-dl-77/chef-oeuvre


create_bucket:
	gsutil mb gs://$(BUCKET_NAME)


clean_bucket:
	gsutil -m rm -r gs://$(BUCKET_NAME)/*
