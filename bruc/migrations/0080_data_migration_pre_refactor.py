from decimal import Decimal, InvalidOperation

from django.db import migrations


def convert_data_forward(apps, schema_editor):
    Guests = apps.get_model('bruc', 'Guests')
    Tags = apps.get_model('bruc', 'Tags')
    Sponsors = apps.get_model('bruc', 'Sponsors')
    Cjenik = apps.get_model('bruc', 'Cjenik')
    Visibility = apps.get_model('bruc', 'Visibility')
    GameLeaderboard = apps.get_model('bruc', 'GameLeaderboard')

    # Guests.bought: normalize all non-'1' values to '0'
    Guests.objects.exclude(bought='1').update(bought='0')

    # Guests.entered: normalize all non-'1' values (including '') to '0'
    Guests.objects.exclude(entered='1').update(entered='0')

    # Tags: ensure numeric string values
    for tag in Tags.objects.all():
        changed = False
        for field in ['count', 'bought', 'entered']:
            val = getattr(tag, field)
            try:
                int(val)
            except (ValueError, TypeError):
                setattr(tag, field, '0')
                changed = True
        if changed:
            tag.save()

    # Sponsors: normalize guestsEnabled and guestCap in one pass
    for s in Sponsors.objects.all():
        changed = False
        if s.guestsEnabled not in ('0', '1', '2'):
            s.guestsEnabled = '1'
            changed = True
        if s.guestCap == '' or s.guestCap is None:
            s.guestCap = None
            changed = True
        else:
            try:
                int(s.guestCap)
            except (ValueError, TypeError):
                s.guestCap = None
                changed = True
        if changed:
            s.save()

    # Cjenik: validate priceEUR (Decimal) and volume (int) in one pass
    for c in Cjenik.objects.all():
        changed = False
        try:
            Decimal(str(c.priceEUR))
        except (InvalidOperation, TypeError):
            c.priceEUR = '0'
            changed = True
        try:
            int(c.volume)
        except (ValueError, TypeError):
            c.volume = '0'
            changed = True
        if changed:
            c.save()

    # Visibility.visible: normalize all non-'1' values to '0'
    Visibility.objects.exclude(visible='1').update(visible='0')

    # Fix NULL/invalid values in already-declared IntegerFields
    schema_editor.execute(
        'UPDATE bruc_sponsors SET "order" = 0 WHERE "order" IS NULL'
    )
    schema_editor.execute(
        'UPDATE bruc_cjenik SET "order" = 0 WHERE "order" IS NULL'
    )
    schema_editor.execute(
        'UPDATE bruc_gameleaderboard SET score = 0 WHERE score IS NULL'
    )


class Migration(migrations.Migration):
    dependencies = [
        ('bruc', '0079_add_sponsor_access_token'),
    ]

    operations = [
        migrations.RunPython(convert_data_forward, migrations.RunPython.noop),
    ]
