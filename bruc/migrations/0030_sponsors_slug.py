# Generated by Django 4.0.4 on 2022-09-14 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bruc', '0029_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsors',
            name='slug',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
