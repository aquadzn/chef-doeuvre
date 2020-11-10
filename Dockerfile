# FROM python:3.8-slim-buster
FROM fastai/fastai:latest

EXPOSE 5000

RUN mkdir -p /app
COPY . /app
WORKDIR /app/

# RUN pip install -r requirements.txt
RUN pip install flask flask-sqlalchemy flask-login ipython

# ENTRYPOINT ["python", "main.py"]
ENTRYPOINT ["make", "run"]


