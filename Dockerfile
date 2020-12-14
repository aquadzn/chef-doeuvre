# MULTI STAGE ~1.3GB
FROM python:3.8-slim AS compile
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

RUN pip install --user -f https://download.pytorch.org/whl/torch_stable.html torch==1.7.0+cpu torchvision==0.8.1+cpu fastai flask flask-sqlalchemy psycopg2-binary flask-login ipython google-cloud-storage requests gunicorn

FROM python:3.8-slim AS build
COPY --from=compile /root/.local /root/.local

RUN mkdir -p /app
COPY . /app
WORKDIR /app

ENV PATH=/root/.local/bin:$PATH
EXPOSE 8080
RUN python create_sample_db.py
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1" ,"--threads", "8", "--timeout", "0" ,"main_gcp:app"]
