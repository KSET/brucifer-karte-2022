# Generated by Django 4.0.4 on 2022-09-13 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bruc', '0027_rename_slug_lineup_order_rename_slug_sponsors_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='lineup',
            name='slug',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='tags',
            name='slug',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
