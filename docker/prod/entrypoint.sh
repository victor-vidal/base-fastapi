#!/bin/bash
set -e

echo Starting Uvicorn.
# exec uvicorn app.main:app --host 0.0.0.0 --port 8001 --log-level critical"$@"
# exec uvicorn app.main:app --host 0.0.0.0 --port 8001 --workers 6 --log-level info --worker-class uvicorn.workers.UvicornWorker"$@"
exec gunicorn app.main:app -k uvicorn.workers.UvicornWorker -c deploy_conf.py
# exec python a.py