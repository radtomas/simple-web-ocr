#!/bin/bash
python manage.py makemigrations
python manage.py migrate --noinput
python manage.py initadmin

python manage.py runserver 0.0.0.0:8000