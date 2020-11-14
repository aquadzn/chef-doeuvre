FROM fastai/fastai:latest

EXPOSE 8080

RUN mkdir -p /app

COPY . /app
WORKDIR /app/

RUN pip install flask flask-sqlalchemy psycopg2-binary flask-login ipython google-cloud-storage requests gunicorn
RUN python create_sample_db.py

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1" ,"--threads", "8", "--timeout", "0" ,"main_gcp:app"]