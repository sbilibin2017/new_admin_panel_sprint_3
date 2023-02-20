#!/bin/bash

echo "Waiting for postgres..."
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_DOCKER_HOST $POSTGRES_PORT; do
      sleep 1
    done

    echo "PostgreSQL started"
fi

python3 manage.py migrate --fake 
python3 manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME   

gunicorn -b 0.0.0.0:8000 config.wsgi:application

exec "$@"