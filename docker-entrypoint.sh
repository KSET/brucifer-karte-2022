#!/bin/bash
python manage.py flush --no-input
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata init_data.json
python initadmin.py
python manage.py runserver 0.0.0.0:8000