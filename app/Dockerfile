FROM python:3.9-alpine

LABEL  version="1.0" description="python/app"

WORKDIR    /app

RUN    mkdir -p /app

RUN    pip install --upgrade pip

COPY    requirements.txt /app/

RUN    pip install -r requirements.txt

COPY    ./static    ./static

COPY    ./templates    ./templates

COPY    ./*.py        ./

EXPOSE    80

CMD    ["python", "/app/app.py"]