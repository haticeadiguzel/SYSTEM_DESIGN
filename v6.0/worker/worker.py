from flask_sqlalchemy import SQLAlchemy
from rq import Worker, Connection
from flask import Flask
import subprocess
import redis

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://hatice:ataturk@db_thread_container:5432/system"

redis_host = "redis_thread_container"
redis_port = 6379
redis_db = 0

conn = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
db = SQLAlchemy(app)


class Thread(db.Model):
    __tablename__ = "thread"
    id = db.Column(db.Integer, primary_key=True)
    command = db.Column(db.Text, nullable=False)
    output = db.Column(db.Text, nullable=False)


def run_command(command):
    try:
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        stdout, stderr = process.communicate()
        output = stdout.decode("utf-8") if stdout else stderr.decode("utf-8")

        with app.app_context():
            thread = Thread(command=command, output=output)
            db.session.add(thread)
            db.session.commit()

    except Exception as e:
        print(f"Error running command: {str(e)}")

    return {"status": "success", "output": output}


if __name__ == "__main__":
    with Connection(conn):
        worker = Worker(["default"])
        worker.work()
