from django.db import migrations, models


def to_pending(apps, schema_editor):
    BrucosiFormResponse = apps.get_model('bruc', 'BrucosiFormResponse')
    BrucosiFormResponse.objects.filter(status__in=('invalid', 'valid')).update(status='pending')


def to_invalid(apps, schema_editor):
    BrucosiFormResponse = apps.get_model('bruc', 'BrucosiFormResponse')
    BrucosiFormResponse.objects.filter(status='pending').update(status='invalid')


class Migration(migrations.Migration):

    dependencies = [
        ('bruc', '0089_guests_mail_status_delivered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brucosiformresponse',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('redeemed', 'Redeemed')], default='pending', max_length=10),
        ),
        migrations.RunPython(to_pending, to_invalid),
        migrations.AlterField(
            model_name='guests',
            name='mailStatus',
            field=models.CharField(choices=[('none', 'None'), ('pending', 'Pending'), ('sent', 'Sent'), ('delivered', 'Delivered'), ('failed', 'Failed'), ('bounced', 'Bounced')], default='none', max_length=10),
        ),
    ]
