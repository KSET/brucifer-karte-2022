# Generated by Django 4.0.4 on 2022-09-26 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bruc', '0035_alter_mailer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailer',
            name='message',
            field=models.CharField(default=0, max_length=1000),
        ),
    ]
