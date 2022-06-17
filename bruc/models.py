from django.db import models

# Create your models here.

class Guests(models.Model):
    id=models.CharField(max_length=50, primary_key=True, default='', blank=True)
    name=models.CharField(max_length=50, default='', blank=True)
    surname=models.CharField(max_length=50, default='', blank=True)
    jmbag=models.CharField(max_length=50, default='', blank=True)
    phone=models.CharField(max_length=50, default='', blank=True)
    tag=models.CharField(max_length=50, default='', blank=True)
    bought=models.CharField(max_length=50, default='0', blank=True)
    entered=models.CharField(max_length=50, default='', blank=True)
    deleted=models.CharField(max_length=50, default='', blank=True)

class Users(models.Model):
    id=models.CharField(max_length=50, primary_key=True, default='', blank=True)
    name=models.CharField(max_length=50, default='', blank=True)
    email=models.CharField(max_length=50, default='', blank=True)
    privilege=models.CharField(max_length=50, default='', blank=True)

class Tags(models.Model):
    id=models.CharField(max_length=50, primary_key=True, default=0, blank=False)
    name=models.CharField(max_length=49, default='', blank=True)
    count=models.CharField(max_length=50, default='0', blank=True)
    bought=models.CharField(max_length=50, default='0', blank=True)
    entered=models.CharField(max_length=50, default='0', blank=True)



