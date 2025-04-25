import multiprocessing

# Gunicorn config variables
workers = multiprocessing.cpu_count() * 2 + 1
bind = "0.0.0.0:8000"
keepalive = 120
timeout = 120
worker_class = "uvicorn.workers.UvicornWorker" 