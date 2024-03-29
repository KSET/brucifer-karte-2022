# Generated by Django 4.0.4 on 2022-06-17 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bruc', '0020_users_id_alter_tags_id_alter_users_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lineup',
            fields=[
                ('id', models.CharField(default=0, max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, default='', max_length=49)),
                ('url', models.CharField(blank=True, default='0', max_length=50)),
                ('image', models.ImageField(blank=True, default='0', max_length=50, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Sponsors',
            fields=[
                ('id', models.CharField(default=0, max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, default='', max_length=49)),
                ('url', models.CharField(blank=True, default='0', max_length=50)),
                ('image', models.ImageField(blank=True, default='0', max_length=50, upload_to='')),
            ],
        ),
        migrations.AlterField(
            model_name='tags',
            name='name',
            field=models.CharField(blank=True, default='', max_length=49),
        ),
    ]
