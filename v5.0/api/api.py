from flask import request, jsonify, json
import platform
import subprocess
import os
from worker import run_command, Thread, db, app, queue


def thread_serializer(thread):
    return {"id": thread.id, "command": thread.command, "output": thread.output}


@app.route("/thread", methods=["GET"])
def index():
    return jsonify([*map(thread_serializer, Thread.query.all())])


@app.route("/get_os", methods=["GET"])
def get_os():
    try:
        operating_system = platform.system()
        current_directory = os.getcwd()
        try:
            client = os.getlogin() #local
        except:
            client = request.environ.get("HTTP_X_REAL_IP", request.remote_addr) #docker

        prompt_directory = f"{client}@{operating_system}:{current_directory}$ "
        return jsonify({"prompt_directory": prompt_directory})
    except:
        prompt_directory = ">>>"
        return prompt_directory


@app.route("/thread/create", methods=["POST"])
def create():
    request_data = json.loads(request.data)
    command = request_data["command"]

    process = subprocess.Popen(
            ["ls"] , stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
    stdout, stderr = process.communicate()
    output = stdout.decode("utf-8")
    error = stderr.decode("utf-8")

    # if command == "clear":
    #     Thread.query.delete()
    #     db.session.commit()
    #     return jsonify({"status": "success", "message": "threads deleted successfully"})

    # if command.startswith("cd"):
    #     if len(command) == 2:
    #         os.chdir(os.path.expanduser("/"))
    #     else:
    #         new_directory = command[3:]
    #         try:
    #             os.chdir(new_directory)
    #         except FileNotFoundError:
    #             return jsonify(
    #                 {
    #                     "status": "error",
    #                     "message": f"Directory not found: {new_directory}",
    #                 }
    #             )
    # run_command(command)
    # job = queue.enqueue(run_command, command)
    # print(f"Job: {job.get_id()}")
    return jsonify({"status": output, "message": error})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
