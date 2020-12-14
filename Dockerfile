# MULTI STAGE ~1.3GB
FROM python:3.8-slim AS compile
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install -f https://download.pytorch.org/whl/torch_stable.html torch==1.7.0+cpu torchvision==0.8.1+cpu fastai flask flask-sqlalchemy psycopg2-binary flask-login ipython google-cloud-storage requests gunicorn

FROM python:3.8-slim AS build
COPY --from=compile /opt/venv /opt/venv
COPY . .

EXPOSE 8080

ENV PATH="/opt/venv/bin:$PATH"

RUN python create_sample_db.py
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1" ,"--threads", "8", "--timeout", "0" ,"main_gcp:app"]
