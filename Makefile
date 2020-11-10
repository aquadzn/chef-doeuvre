HOST=127.0.0.1
PORT=5000

setup:
	pip install -r requirements.txt

lint:
	black *.py

run:
	python main.py --host $(HOST) --port $(PORT)

docker:
	docker build -t chef-oeuvre .