FROM fastai/fastai:latest

EXPOSE 8080

RUN mkdir -p /app

COPY . /app
WORKDIR /app/

RUN pip install flask flask-sqlalchemy flask-login ipython requests gunicorn flake8 black pytest bandit google-cloud-storage
RUN make lint && make test

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1" ,"--threads", "8", "--timeout", "0" ,"main_gcp:app"]