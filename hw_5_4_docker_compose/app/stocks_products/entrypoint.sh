#! /bin/bash

python manage.py migrate

python manage.py collectstatic

#python manage.py runserver 0.0.0.0:8000
exec gunicorn stocks_products.wsgi:application -b 0.0.0.0:8000 --reload