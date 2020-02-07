"""gunicorn server configuration."""
import os

bind = f":{os.environ.get('PORT', '8080')}"
workers = 1
threads = 2
timeout = 30
worker_class = 'uvicorn.workers.UvicornWorker'
