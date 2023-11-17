from rq import Worker, Queue, Connection
import subprocess
import requests
import redis

redis_host = "redis_thread_container"
redis_port = 6379
redis_db = 0
conn = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)

def run_command(command):
    try:
        process = subprocess.Popen(
            ["ls"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        stdout, stderr = process.communicate()
        output = stdout.decode("utf-8")
        error = stderr.decode("utf-8")

        print(f"Output: {output}")
        print(f"Error: {error}")

        # data = {
        #     "output": output,
        #     "error": error
        # }

        # response = requests.post("http://api_thread_container:5000/send_data", json=data)

        # if response.status_code != 200:
        #     print(f"Error sending data: {response.status_code}")
        # else:
        #     print(f"Data sent, server responded with: {response.text}")

    except Exception as e:
        print(f"Error running command: {str(e)}")

    return {"status": "success2", "output": output, "error": error}


if __name__ == "__main__":
    with Connection(conn):
        print(f"Connection: {Connection(conn)}")
        worker = Worker(["default"])
        worker.work()
        print("Worker worked")
