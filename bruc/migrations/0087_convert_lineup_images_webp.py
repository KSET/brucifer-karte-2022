from django.db import migrations

from bruc.images import to_webp


def forwards(apps, schema_editor):
    Lineup = apps.get_model('bruc', 'Lineup')
    for row in Lineup.objects.exclude(image='').exclude(image__isnull=True):
        old_name = row.image.name
        if old_name.lower().endswith('.webp'):
            continue
        storage = row.image.storage
        if not storage.exists(old_name):
            print(f'\n  [lineup {row.pk}] missing file, skipped: {old_name}')
            continue
        try:
            old_size = storage.size(old_name)
            with storage.open(old_name, 'rb') as f:
                webp = to_webp(f)
            if webp is None:
                continue
            row.image.save(webp.name, webp, save=False)
            row.save(update_fields=['image'])
            storage.delete(old_name)
            print(f'\n  [lineup {row.pk}] {old_name} ({old_size // 1024} KB)'
                  f' -> {row.image.name} ({storage.size(row.image.name) // 1024} KB)')
        except Exception as e:
            print(f'\n  [lineup {row.pk}] failed, kept original {old_name}: {e}')


class Migration(migrations.Migration):

    dependencies = [
        ('bruc', '0086_remove_brucosiformresponse_email'),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
