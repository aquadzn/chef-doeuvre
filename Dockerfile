FROM fastai/fastai:latest

EXPOSE 8000

RUN mkdir -p /app
COPY . /app
WORKDIR /app/

RUN pip install flask flask-sqlalchemy flask-login ipython

ENTRYPOINT ["make", "run", "HOST=0.0.0.0", "PORT=8000"]
