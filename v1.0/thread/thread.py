from flask import Flask, jsonify, request, json
from flask_sqlalchemy import SQLAlchemy
import subprocess
import os
import platform
import redis

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://hatice:ataturk@172.17.0.2:5432/system"
db = SQLAlchemy(app)

redis_host = "172.17.0.4"
redis_port = 6379
redis_db = 0
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    command = db.Column(db.Text, nullable=False)
    output = db.Column(db.Text, nullable=False)

    def __str__(self) -> str:
        return f"{self.id} {self.command} {self.output}"

    def to_dict(self):
        return {"id": self.id, "command": self.command, "output": self.output}


def thread_serializer(thread):
    return {"id": thread.id, "command": thread.command, "output": thread.output}


@app.route("/thread", methods=["GET"])
def index():
    return jsonify([*map(thread_serializer, Thread.query.all())])


@app.route("/get_os", methods=["GET"])
def get_os():
    operating_system = platform.system()
    while True:
        user_hatice = os.getlogin()
        current_directory = os.getcwd()
        prompt_directory = f"{user_hatice}@{operating_system}:{current_directory}$ "

        return jsonify({"prompt_directory": prompt_directory})


@app.route("/thread/create", methods=["POST"])
def create():
    request_data = json.loads(request.data)
    command = request_data["command"]

    if command == "clear":
        Thread.query.delete()
        db.session.commit()
        return jsonify({"status": "success", "message": "thread deleted successfully"})

    if command.startswith("cd"):
        if len(command) == 2:
            os.chdir(os.path.expanduser("~"))
        else:
            new_directory = command[3:]
            try:
                os.chdir(new_directory)
            except FileNotFoundError:
                print(f"Directory not found: {new_directory}")

    try:
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        stdout, stderr = process.communicate()
        output = stdout.decode("utf-8")
        error = stderr.decode("utf-8")

        if output:
            thread = Thread(command=command, output=output)
        else:
            thread = Thread(command=command, output=error)

        db.session.add(thread)
        db.session.commit()

        redis_client.set(command, output)

        value = redis_client.get(command)

        if value is not None:
            print(f"Value from Redis: {value.decode('utf-8')}")
        else:
            print("Value not found in Redis")

        return jsonify({"status": "success", "message": "thread created successfully"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
