# Gunicorn configuration file
# https://docs.gunicorn.org/en/stable/configure.html#configuration-file
# https://docs.gunicorn.org/en/stable/settings.html

import multiprocessing

bind = ":3001"
# Concerning `workers` setting see:
# https://github.com/wemake-services/wemake-django-template/issues/1022
workers = multiprocessing.cpu_count() * 2 + 1

max_requests = 2000
max_requests_jitter = 400

timeout = 3600
worker_class = "gevent"
worker_connections = 1000
graceful_timeout = 60

log_file = "-"
chdir = "/app"
worker_tmp_dir = "/dev/shm"  # noqa: S108
