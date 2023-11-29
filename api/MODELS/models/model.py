from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import redis

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://hatice:ataturk@db_thread_container:5432/system"

redis_host = "redis_thread_container"
redis_port = 6379
redis_db = 0

db = SQLAlchemy(app)
conn = redis.Redis(host=redis_host, port=redis_port, db=redis_db)


class Thread(db.Model):
    __tablename__ = "thread"
    id = db.Column(db.Integer, primary_key=True)
    command = db.Column(db.Text, nullable=False)
    output = db.Column(db.Text, nullable=True)
    directory = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
