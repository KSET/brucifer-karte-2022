# Generated by Django 4.0.4 on 2022-10-30 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bruc', '0047_alter_mailer_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guests',
            name='tag',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]