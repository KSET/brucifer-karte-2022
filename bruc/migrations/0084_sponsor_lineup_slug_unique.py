from collections import defaultdict
from uuid import uuid4

from django.db import migrations, models
from django.db.models import Q

def _dedupe(apps, model_name):
    Model = apps.get_model("bruc", model_name)

    groups = defaultdict(list)
    for row in Model.objects.only("id", "slug"):
        groups[row.slug].append(row)

    for slug, rows in groups.items():
        if len(rows) < 2 and slug:
            continue
        rows.sort(key=lambda r: r.id)
        start = 1 if slug else 0
        for dup in rows[start:]:
            dup.slug = str(uuid4())
            dup.save(update_fields=["slug"])


def dedupe_slugs(apps, schema_editor):
    _dedupe(apps, "Sponsors")
    _dedupe(apps, "Lineup")


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("bruc", "0083_users_email_unique"),
    ]

    operations = [
        migrations.RunPython(dedupe_slugs, noop_reverse),
        migrations.AddConstraint(
            model_name="sponsors",
            constraint=models.UniqueConstraint(
                condition=~Q(slug=""),
                fields=("slug",),
                name="uniq_sponsors_slug_nonblank",
            ),
        ),
        migrations.AddConstraint(
            model_name="lineup",
            constraint=models.UniqueConstraint(
                condition=~Q(slug=""),
                fields=("slug",),
                name="uniq_lineup_slug_nonblank",
            ),
        ),
    ]
