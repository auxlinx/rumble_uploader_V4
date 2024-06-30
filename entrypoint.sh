#!/bin/sh

python /code/manage.py makemigrations
python /code/manage.py migrate
exec "$@"
