from flask import request, jsonify, json, Flask
from flask_sqlalchemy import SQLAlchemy
from rq import Queue
import platform
import redis
import os

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://hatice:ataturk@db_thread_container:5432/system"

redis_host = "redis_thread_container"
redis_port = 6379
redis_db = 0

db = SQLAlchemy(app)
conn = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
queue = Queue(connection=conn)


class Thread(db.Model):
    __tablename__ = "thread"
    id = db.Column(db.Integer, primary_key=True)
    command = db.Column(db.Text, nullable=False)
    output = db.Column(db.Text, nullable=False)


with app.app_context():
    db.create_all()
    db.session.commit()


def thread_serializer(thread):
    return {"id": thread.id, "command": thread.command, "output": thread.output}


@app.route("/thread", methods=["GET"])
def index():
    threads = Thread.query.all()
    max_clear_id = None
    filtered_threads = []

    for thread in threads:
        if thread.command == "clear":
            if max_clear_id is None or thread.id > max_clear_id:
                max_clear_id = thread.id

    if max_clear_id is not None:
        filtered_threads = Thread.query.filter(Thread.id > max_clear_id).all()
    else:
        filtered_threads = Thread.query.all()

    print(filtered_threads)

    return jsonify([thread_serializer(thread) for thread in filtered_threads])


@app.route("/get_os", methods=["GET"])
def get_os():
    try:
        operating_system = platform.system()
        try:
            client = os.getlogin()  # local environment
        except:
            client = request.environ.get(
                "HTTP_X_REAL_IP", request.remote_addr
            )  # docker environment

        prompt_directory = f"{client}@{operating_system}$ "
        return jsonify({"prompt_directory": prompt_directory})
    except Exception as e:
        print(f"Error in get_os: {e}")
        prompt_directory = ">>>"
        return jsonify({"prompt_directory": prompt_directory})


@app.route("/thread/create", methods=["POST"])
def create():
    try:
        request_data = json.loads(request.data)
        command = request_data["command"]

        queue.enqueue("worker.run_command", command)
        return jsonify({"status": "success"})

    except Exception as e:
        print(f"Error in create: {e}")
        return jsonify({"status": "error", "message": str(e)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
