from rq import Worker, Queue, Connection
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify
import subprocess
import redis

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://hatice:ataturk@172.17.0.2:5432/system"
db = SQLAlchemy(app)

redis_host = "172.17.0.4"
redis_port = 6379
redis_db = 0
conn = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)
queue = Queue(connection=conn)

class Thread(db.Model):
    __tablename__ = "thread"
    id = db.Column(db.Integer, primary_key=True)
    command = db.Column(db.Text, nullable=False)
    output = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()
    db.session.commit()

def run_command(command):
    print(f"Runcommand")
    try:
        process = subprocess.Popen(
            command, stdout = subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        stdout, stderr = process.communicate()
        output = stdout.decode("utf-8")
        error = stderr.decode("utf-8")
        conn.set(command, command)
        if output:
            thread = Thread(command=command, output=output)
            conn.set(output, output)
        else:
            thread = Thread(command=command, output=error)
            conn.set(output, error)

        with app.app_context():
            db.session.add(thread)
            db.session.commit()
            value1 = conn.get(command)
            print(f"Redis Command: {value1}")
            value2 = conn.get(output)
            print(f"Redis Output: {value2}")
            
            return jsonify({"status": "success", "message": "thread created successfully"})     

    except Exception as e:
        print(f"Error running command: {str(e)}")

if __name__ == "__main__":
    with Connection(conn):
        print(f"Connection: {Connection(conn)}")
        worker = Worker([queue])
        worker.work()
        print("Worker worked")