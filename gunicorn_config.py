"""gunicorn server configuration."""
import os

bind = f":{os.environ.get('PORT', '8080')}"
threads = 2
workers = 4
timeout = 60
worker_class = 'uvicorn.workers.UvicornWorker'
