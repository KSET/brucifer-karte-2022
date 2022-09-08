#!/bin/bash
python manage.py flush --no-input
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata initial_MK2ZK_data.json
python manage.py runserver 0.0.0.0:8000