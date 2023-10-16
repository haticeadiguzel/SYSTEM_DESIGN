FROM python:3

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

RUN pip install psycopg2-binary

COPY . .

CMD ["python", "thread.py"]