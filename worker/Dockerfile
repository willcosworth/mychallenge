FROM python:3.9-alpine

LABEL  version="1.0" description="python/worker"

WORKDIR    /worker

RUN    mkdir -p /worker

RUN    pip install --upgrade pip

COPY    requirements.txt /worker/

RUN    pip install -r requirements.txt

COPY    ./*.py        ./

CMD    ["python", "/worker/worker.py"]
