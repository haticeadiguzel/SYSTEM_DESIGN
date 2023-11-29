from models.model import Thread, db, app, conn
from rq import Worker, Connection
import subprocess
import os


def run_command(command):
    try:
        with app.app_context():
            thread_directory = Thread.query.order_by(Thread.id.desc()).first()
            working_directory = thread_directory.directory
            print("working directory: ", working_directory)

        os.chdir(working_directory)

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            cwd=working_directory,
        )
        stdout, stderr = process.communicate()
        output = stdout.decode("utf-8") if stdout else stderr.decode("utf-8")

        with app.app_context():
            thread = (
                Thread.query.filter_by(command=command, directory=working_directory)
                .order_by(Thread.id.desc())
                .first()
            )
            if thread:
                thread.output = output
                db.session.commit()

    except Exception as e:
        print(f"Error running command: {str(e)}")

    return {"status": "success"}


if __name__ == "__main__":
    with Connection(conn):
        worker = Worker(["default"])
        worker.work()
