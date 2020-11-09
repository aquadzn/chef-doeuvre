FROM python:3.8-slim

EXPOSE 5000

RUN mkdir -p /app
COPY . /app
WORKDIR /app/

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "app.py"]