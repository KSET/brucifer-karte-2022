#!/usr/bin/env python
from dotenv import load_dotenv

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "brucifer.settings")

import django
django.setup()

from django.contrib.auth.models import User
load_dotenv()
User.objects.create_superuser(os.getenv("DJANGO_ADMIN_USER"),os.getenv("DJANGO_ADMIN_EMAIL"),os.getenv("DJANGO_ADMIN_PASS"))