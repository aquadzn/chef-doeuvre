FROM python:3.8-slim-buster

EXPOSE 5000

RUN mkdir -p /app
COPY . /app
WORKDIR /app/

RUN python3 -m pip install -r requirements.txt

ENTRYPOINT ["python3", "app.py"]