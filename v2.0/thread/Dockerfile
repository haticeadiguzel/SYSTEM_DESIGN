# syntax=docker/dockerfile:1
FROM python:3

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

COPY . .

ENTRYPOINT [ "python" ]

CMD [ "thread.py" ]