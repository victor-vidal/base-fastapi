import multiprocessing
import os

print(f"ENVIRONMENT {os.environ.get('ENVIRONMENT')}")
if os.environ.get("ENVIRONMENT") == "development":
    workers = 1
    reload = True
else:
    # workers = multiprocessing.cpu_count()
    workers = 1

print(f"Fast API Auth Server - Num Workers: {workers}")

bind = "0.0.0.0:8000"
keepalive = 120
errorlog = "-"
pidfile = "/tmp/fastapi.pid"
loglevel = "info"
accesslog = "-"