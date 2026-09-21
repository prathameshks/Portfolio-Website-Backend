#!/bin/bash
set -e

python manage.py collectstatic --noinput
python manage.py migrate --noinput

gunicorn webanalytics.wsgi --bind=0.0.0.0:8000
