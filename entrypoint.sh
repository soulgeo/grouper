#!/bin/sh

echo "Restoring HTMX..."
npm run copy-htmx

echo "Collecting static files..."
python src/manage.py collectstatic --noinput --clear

echo "Running migrations..."
python src/manage.py migrate

echo "Starting server..."
python src/manage.py runserver 0.0.0.0:8000
