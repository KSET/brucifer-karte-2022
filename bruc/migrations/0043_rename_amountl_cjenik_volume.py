# Generated by Django 4.0.4 on 2022-10-19 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bruc', '0042_cjenik_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cjenik',
            old_name='amountL',
            new_name='volume',
        ),
    ]
