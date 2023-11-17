# syntax=docker/dockerfile:1
FROM python:3

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /app

COPY . .

CMD [ "python", "worker.py" ]