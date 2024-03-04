FROM python:3.9-alpine

LABEL  version="1.0" description="python/api"

WORKDIR    /api

RUN    mkdir -p /api

RUN    pip install --upgrade pip

COPY    requirements.txt /api/

RUN    pip install -r requirements.txt

COPY    ./*.py        ./

EXPOSE    80

CMD    ["python", "/api/api.py"]