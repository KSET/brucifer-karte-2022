from django.db import migrations, models
from django.utils import timezone
from django.utils.dateparse import parse_datetime


TIME_ROWS = ("TIMER_TIME", "SPONSORS_INPUT_TIME")


def backfill_time_rows(apps, schema_editor):
    Visibility = apps.get_model("bruc", "Visibility")
    table = Visibility._meta.db_table

    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            "SELECT name, CAST(visible AS TEXT) FROM {} WHERE name IN (%s, %s)".format(
                table
            ),
            TIME_ROWS,
        )
        raw_rows = dict(cursor.fetchall())

    default_zone = timezone.get_default_timezone()

    for name in TIME_ROWS:
        if name not in raw_rows:
            Visibility.objects.create(name=name, visible=False, time=None)
            continue

        raw = raw_rows[name]
        parsed = parse_datetime(raw) if isinstance(raw, str) else None
        if parsed is None:
            continue
        if timezone.is_naive(parsed):
            parsed = timezone.make_aware(parsed, default_zone)
        Visibility.objects.filter(name=name).update(time=parsed)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("bruc", "0084_sponsor_lineup_slug_unique"),
    ]

    operations = [
        migrations.AddField(
            model_name="visibility",
            name="time",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.RunPython(backfill_time_rows, noop_reverse),
    ]
