import multiprocessing
import os

# Gunicorn config variables
workers = multiprocessing.cpu_count() * 2 + 1
bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"  # Use PORT from environment or default to 8000
keepalive = 120
timeout = 120
worker_class = "uvicorn.workers.UvicornWorker" 