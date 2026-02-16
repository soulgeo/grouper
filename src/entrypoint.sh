#!/bin/sh

export DJANGO_SETTINGS_MODULE=grouper.settings

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Running migrations..."
python manage.py migrate

echo "Starting server..."
if [ "$DEBUG" = "True" ]; then
    python manage.py runserver 0.0.0.0:8000
else
    daphne -b 0.0.0.0 -p 8000 grouper.asgi:application
fi
