FROM fastai/fastai:latest

EXPOSE 8000

RUN mkdir -p /app
COPY . /app
WORKDIR /app/

RUN pip install flask flask-sqlalchemy flask-login ipython gunicorn flake8 black pytest google-cloud-storage
RUN make lint && make test

CMD exec gunicorn --bind :$(PORT) --workers 1 --threads 8 --timeout 0 main:app