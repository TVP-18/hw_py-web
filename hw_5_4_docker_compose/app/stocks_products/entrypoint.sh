#! /bin/bash

python manage.py migrate
#python manage.py runserver 0.0.0.0:8000
exec gunicorn stocks_products.msgi:application -b 0.0.0.0:8000 --reload
