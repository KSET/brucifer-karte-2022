from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete

# Create your models here.


class Guests(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default='', blank=True)
    surname = models.CharField(max_length=50, default='', blank=True)
    jmbag = models.CharField(max_length=50, default='', blank=True)
    email = models.CharField(max_length=50, default='', blank=True)
    tag = models.CharField(max_length=200, default='', blank=True)
    bought = models.CharField(max_length=50, default='0', blank=True)
    entered = models.CharField(max_length=50, default='', blank=True)
    confCode = models.CharField(max_length=50, default='', blank=True)


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default='', blank=True)
    email = models.CharField(max_length=50, default='', blank=True)
    privilege = models.CharField(max_length=50, default='', blank=True)


class Tags(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.CharField(max_length=200, default='', blank=True)
    name = models.CharField(max_length=49, default='', blank=True)
    count = models.CharField(max_length=50, default='0', blank=True)
    bought = models.CharField(max_length=50, default='0', blank=True)
    entered = models.CharField(max_length=50, default='0', blank=True)


class Lineup(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.CharField(max_length=200, default='', blank=True)
    order = models.IntegerField(default='', blank=True)
    visible = models.CharField(max_length=200, default='', blank=True)
    name = models.CharField(max_length=49, default='', blank=True)
    image = models.ImageField(
        upload_to='uploads/lineup', blank=True, null=True)

    '''def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return '' '''

    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, path = self.image.storage, self.image.path
        # Delete the model before the file
        super(Lineup, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)


class Sponsors(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.CharField(max_length=200, default='', blank=True)
    order = models.IntegerField(default='', blank=True)
    visible = models.CharField(max_length=200, default='', blank=True)
    guestsEnabled = models.CharField(max_length=200, default='1', blank=True)
    name = models.CharField(max_length=49, default='', blank=True)
    url = models.CharField(max_length=400, default='0', blank=True)
    image = models.ImageField(
        upload_to='uploads/sponsors', blank=True, null=True)
    email = models.CharField(max_length=20000, default='', blank=True)
    guestCap = models.CharField(max_length=49, default='', blank=True)

    '''def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return '' '''

    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, path = self.image.storage, self.image.path
        # Delete the model before the file
        super(Sponsors, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)


class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    bandName = models.CharField(max_length=49, default='', blank=True)
    bookerName = models.CharField(max_length=50, default='0', blank=True)
    bookerPhone = models.CharField(max_length=50, default='0', blank=True)


class Mailer(models.Model):
    subject = models.CharField(max_length=20000, default=0, blank=False)
    message = models.CharField(max_length=20000, default=0, blank=False)
    to_mail = models.CharField(max_length=20000, default=0, blank=False)


class Cjenik(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='', blank=True)
    tag = models.CharField(max_length=50, default='0', blank=True)
    order = models.IntegerField(default='', blank=True)
    priceEUR = models.CharField(max_length=50, default='0', blank=True)
    volume = models.CharField(max_length=50, default='0', blank=True)


class Visibility(models.Model):
    name = models.CharField(max_length=100, default='',
                            blank=True, primary_key=True)
    visible = models.CharField(max_length=50, default='0', blank=True)


class Translations(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=5000, default='', blank=True)
    value = models.CharField(max_length=5000, default='', blank=True)

class GameLeaderboard(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default='', blank=True)
    email = models.CharField(max_length=50, default='', blank=True)
    score = models.IntegerField(default='', blank=True)