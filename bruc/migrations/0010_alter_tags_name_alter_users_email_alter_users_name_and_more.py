# Generated by Django 4.0.4 on 2022-05-24 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bruc', '0009_alter_guests_id_alter_users_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tags',
            name='name',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='users',
            name='name',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='users',
            name='privilege',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
