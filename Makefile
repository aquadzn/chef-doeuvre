HOST=0.0.0.0
PORT=8080
BUCKET_NAME=chef-oeuvre


setup:
	pip install -r requirements.txt


lint:
	black *.py


run:
	python main.py --host $(HOST) --port $(PORT)


build_docker:
	docker build -t chef-oeuvre .


deploy_gcp:
	gcloud builds submit --tag gcr.io/ml-dl-77/chef-oeuvre
	gcloud run deploy "$tag" \
		--image gcr.io/ml-dl-77/chef-oeuvre \
		--platform=managed \
		--allow-unauthenticated \
		--region=us-east1 \
		--concurrency=1 \
		--memory=2Gi


bucket_gcp:
	gsutil mb gs://$(BUCKET_NAME)
