# Generated by Django 4.0.4 on 2022-09-29 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bruc', '0036_alter_mailer_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsors',
            name='visible',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
