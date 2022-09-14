#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

# We are using `gunicorn` for production, see:
# http://docs.gunicorn.org/en/stable/configure.html

# Run python specific scripts:
# Running migrations in startup script might not be the best option, see:
# docs/pages/template/production-checklist.rst
python /app/manage.py migrate
python /app/manage.py loaddata penyakit puskesmas
# python /app/manage.py collectstatic --noinput --clear
echo "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() == False and User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

# Start gunicorn:
# Docs: http://docs.gunicorn.org/en/stable/settings.html
# Make sure it is in sync with `django/ci.sh` check:
gunicorn \
    --config python:gunicorn_config \
    baksos.wsgi
