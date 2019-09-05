#!/bin/sh

echo "Waiting for PostgreSQL to start..."

while ! nc -z weathers-db 5432; do
  sleep 0.1
done

echo "PostgreSQL has started!"

python manage.py run -h 0.0.0.0