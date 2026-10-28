from django.db import migrations, models

from bruc.search import search_key


def backfill(apps, schema_editor):
    Guests = apps.get_model('bruc', 'Guests')
    guests = list(Guests.objects.only('id', 'name', 'surname'))
    for guest in guests:
        guest.searchKey = search_key(guest.name, guest.surname)
    Guests.objects.bulk_update(guests, ['searchKey'], batch_size=500)


class Migration(migrations.Migration):

    dependencies = [
        ('bruc', '0091_sponsor_guests_fk_and_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='guests',
            name='searchKey',
            field=models.TextField(blank=True, default='', editable=False),
        ),
        migrations.RunPython(backfill, migrations.RunPython.noop),
    ]
