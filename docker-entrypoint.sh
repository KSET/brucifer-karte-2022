#!/bin/bash
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
python initadmin.py
python manage.py flushexpiredtokens
exec python manage.py runserver 0.0.0.0:8000
