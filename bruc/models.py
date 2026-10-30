import secrets

from django.db import models, transaction
from django.db.models import Q
from django.dispatch import receiver
from django.db.models.signals import post_delete

from .images import to_webp
from .roles import Role
from .search import search_key

# Create your models here.


class GuestsQuerySet(models.QuerySet):
    """Keeps Guests.searchKey in step with name and surname on the writes that skip save()."""
    NAME_FIELDS = {'name', 'surname'}

    def bulk_create(self, objs, *args, **kwargs):
        objs = list(objs)
        for guest in objs:
            guest.update_search_key()
        return super().bulk_create(objs, *args, **kwargs)

    def bulk_update(self, objs, fields, *args, **kwargs):
        if self.NAME_FIELDS & set(fields):
            objs = list(objs)
            for guest in objs:
                guest.update_search_key()
            return self.model._base_manager.using(self.db).bulk_update(objs, {*fields, 'searchKey'}, *args, **kwargs)
        return super().bulk_update(objs, fields, *args, **kwargs)

    def update(self, **kwargs):
        if 'searchKey' in kwargs:
            raise ValueError('Guests.searchKey is derived from name and surname; leave it out of update()')
        if not self.NAME_FIELDS & kwargs.keys():
            return super().update(**kwargs)
        with transaction.atomic(using=self.db):
            pks = list(self.select_for_update().values_list('pk', flat=True))
            rows = self.model._base_manager.using(self.db).filter(pk__in=pks)
            updated = rows.update(**kwargs)
            guests = list(rows.only('pk', 'name', 'surname'))
            for guest in guests:
                guest.update_search_key()
            rows.bulk_update(guests, ['searchKey'])
        return updated


class Guests(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='', blank=True)
    surname = models.CharField(max_length=50, default='', blank=True)
    jmbag = models.CharField(max_length=50, default='', blank=True)
    email = models.CharField(max_length=50, default='', blank=True)
    tag = models.CharField(max_length=200, default='', blank=True)
    bought = models.BooleanField(default=False)
    entered = models.BooleanField(default=False)
    confCode = models.CharField(max_length=50, default='', blank=True)
    boughtTicketTime = models.DateTimeField(null=True, blank=True)

    MAIL_STATUS_CHOICES = [
        ('none', 'None'),
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
        ('bounced', 'Bounced'),
    ]
    mailStatus = models.CharField(max_length=10, choices=MAIL_STATUS_CHOICES, default='none')
    mailError = models.CharField(max_length=200, default='', blank=True)
    mailSentAt = models.DateTimeField(null=True, blank=True)
    mailMessageId = models.CharField(max_length=255, default='', blank=True)
    sponsor = models.ForeignKey('Sponsors', null=True, blank=True, on_delete=models.SET_NULL, related_name='guests')
    searchKey = models.TextField(default='', blank=True, editable=False)

    objects = GuestsQuerySet.as_manager()

    def update_search_key(self):
        self.searchKey = search_key(self.name, self.surname)

    def save(self, *args, **kwargs):
        self.update_search_key()
        update_fields = kwargs.get('update_fields')
        if update_fields is not None and {'name', 'surname'} & set(update_fields):
            kwargs['update_fields'] = {*update_fields, 'searchKey'}
        super().save(*args, **kwargs)


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default='', blank=True)
    email = models.EmailField(max_length=254, default='', blank=True)
    privilege = models.CharField(
        max_length=50, choices=Role.choices, default=Role.NONE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['email'],
                condition=~Q(email=''),
                name='uniq_users_email_nonblank',
            )
        ]


class Tags(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.CharField(max_length=200, default='', blank=True)
    name = models.CharField(max_length=49, default='', blank=True)


class Lineup(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.CharField(max_length=200, default='', blank=True)
    order = models.PositiveIntegerField(default=0)
    visible = models.BooleanField(default=False)
    name = models.CharField(max_length=49, default='', blank=True)
    biography = models.TextField(default='', blank=True)
    image = models.ImageField(
        upload_to='uploads/lineup', blank=True, null=True)
    startTime = models.DateTimeField(null=True, blank=True)
    endTime = models.DateTimeField(null=True, blank=True)
    STAGE_CHOICES = [
        ('menza', 'Menza'),
        ('kino', 'Kino'),
        ('elektro', 'Elektro'),
    ]
    stage = models.CharField(max_length=10, choices=STAGE_CHOICES, default='', blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['slug'],
                condition=~Q(slug=''),
                name='uniq_lineup_slug_nonblank',
            )
        ]

    '''def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return '' '''

    def save(self, *args, **kwargs):
        old_name = None
        if self.image and not self.image._committed:
            if self.pk:
                old_name = Lineup.objects.filter(pk=self.pk).values_list('image', flat=True).first()
            webp = to_webp(self.image)
            if webp is not None:
                self.image.save(webp.name, webp, save=False)
        super(Lineup, self).save(*args, **kwargs)
        if old_name and old_name != self.image.name:
            self.image.storage.delete(old_name)

    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, name = self.image.storage, self.image.name
        # Delete the model before the file
        super(Lineup, self).delete(*args, **kwargs)
        # Delete the file after the model
        if name:
            storage.delete(name)


def generate_access_token():
    return secrets.token_urlsafe(32)


SPONSOR_TAG_MARKER = " VIP - Sponzor - "


class Sponsors(models.Model):
    class GuestInput(models.IntegerChoices):
        CLOSED = 0, 'Closed'
        UNTIL_DEADLINE = 1, 'Open until deadline'
        ALWAYS_OPEN = 2, 'Open past deadline'

    id = models.AutoField(primary_key=True)
    slug = models.CharField(max_length=200, default='', blank=True)
    access_token = models.CharField(max_length=64, unique=True, default=generate_access_token)
    order = models.IntegerField(default=0)
    visible = models.BooleanField(default=False)
    guestsEnabled = models.IntegerField(choices=GuestInput.choices, default=GuestInput.UNTIL_DEADLINE)
    name = models.CharField(max_length=49, default='', blank=True)
    url = models.CharField(max_length=400, default='0', blank=True)
    image = models.ImageField(
        upload_to='uploads/sponsors', blank=True, null=True)
    email = models.CharField(max_length=20000, default='', blank=True)
    guestCap = models.IntegerField(null=True, blank=True, default=None)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['slug'],
                condition=~Q(slug=''),
                name='uniq_sponsors_slug_nonblank',
            )
        ]

    @property
    def guest_tag(self):
        return f"{self.slug}{SPONSOR_TAG_MARKER}{self.name}"

    def save(self, *args, **kwargs):
        update_fields = kwargs.get('update_fields')
        if not self.pk or (update_fields is not None and 'name' not in update_fields):
            return super().save(*args, **kwargs)
        with transaction.atomic():
            old_name = Sponsors.objects.select_for_update().filter(pk=self.pk).values_list('name', flat=True).first()
            super().save(*args, **kwargs)
            if old_name is not None and old_name != self.name:
                self.guests.update(tag=self.guest_tag)

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
    order = models.IntegerField(default=0)
    priceEUR = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    volume = models.IntegerField(default=0)


class Visibility(models.Model):
    name = models.CharField(max_length=100, default='',
                            blank=True, primary_key=True)
    visible = models.BooleanField(default=False)
    time = models.DateTimeField(null=True, blank=True)


class Translations(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=5000, default='', blank=True)
    value = models.CharField(max_length=500000, default='', blank=True)

class GameLeaderboard(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default='', blank=True)
    email = models.CharField(max_length=50, default='', blank=True)
    score = models.IntegerField(default=0)

class BrucosiFormResponse(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    jmbag = models.CharField(max_length=20)
    gdpr_accepted = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('redeemed', 'Redeemed'),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )