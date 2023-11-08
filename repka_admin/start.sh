#!/bin/bash

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
done 

python3.10 application/manage.py migrate --noinput || exit 1
python3.10 application/manage.py collectstatic --noinput
# chmod 777 application/static/
# chmod 777 application/static/admin/
uwsgi --strict --ini application/uwsgi.ini