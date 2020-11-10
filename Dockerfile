FROM fastai/fastai:latest

EXPOSE 8000

RUN mkdir -p /app
COPY . /app
WORKDIR /app/

RUN pip install flask flask-sqlalchemy flask-login ipython gunicorn google-cloud-storage

CMD gunicorn --bind :$(PORT) --workers 1 --threads 8 --timeout 0 main:app