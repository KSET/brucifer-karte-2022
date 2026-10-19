import secrets
from collections import Counter
from uuid import uuid4

import django.db.models.deletion
from django.db import migrations, models
from django.db.models import Q

import bruc.models

TOKEN_MAX_LENGTH = 64 
MARKER = " VIP - Sponzor - "


def backfill(apps, schema_editor):
    Sponsors = apps.get_model('bruc', 'Sponsors')
    Guests = apps.get_model('bruc', 'Guests')

    sponsors = list(Sponsors.objects.all())
    blank_names = Counter(s.name for s in sponsors if not s.slug)

    seen = set()
    for sponsor in sponsors:
        # Keep already-sent links working; only replace tokens that are blank, duplicate or won't fit.
        token = sponsor.access_token
        if not token or token in seen or len(token) > TOKEN_MAX_LENGTH:
            sponsor.access_token = secrets.token_urlsafe(32)
            sponsor.save(update_fields=['access_token'])
        seen.add(sponsor.access_token)

        if not sponsor.slug:
            # Legacy blank-slug sponsor: its guests are tagged ' VIP - Sponzor - <name>' (DRF may have stripped
            # the space). Link them by name when unambiguous, then give the sponsor a real slug and retag.
            if blank_names[sponsor.name] == 1:
                legacy_tag = f"{MARKER}{sponsor.name}"
                Guests.objects.filter(
                    Q(tag=legacy_tag) | Q(tag=legacy_tag.strip()), sponsor__isnull=True,
                ).update(sponsor=sponsor)
            sponsor.slug = str(uuid4())
            sponsor.save(update_fields=['slug'])
            Guests.objects.filter(sponsor=sponsor).update(tag=f"{sponsor.slug}{MARKER}{sponsor.name}")
            continue

        Guests.objects.filter(sponsor__isnull=True, tag__istartswith=f"{sponsor.slug} ").update(sponsor=sponsor)


def flush_deferred_constraints(apps, schema_editor):
    # PostgreSQL refuses ALTER TABLE while the backfill's deferred FK checks are pending; run them now.
    if schema_editor.connection.vendor == 'postgresql':
        schema_editor.execute("SET CONSTRAINTS ALL IMMEDIATE")


class Migration(migrations.Migration):

    dependencies = [
        ('bruc', '0090_brucosi_status_pending_mail_pending'),
    ]

    operations = [
        migrations.AddField(
            model_name='guests',
            name='sponsor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='guests', to='bruc.sponsors'),
        ),
        migrations.AlterField(
            model_name='sponsors',
            name='guestsEnabled',
            field=models.IntegerField(choices=[(0, 'Closed'), (1, 'Open until deadline'), (2, 'Open past deadline')], default=1),
        ),
        migrations.RunPython(backfill, migrations.RunPython.noop),
        migrations.RunPython(flush_deferred_constraints, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='sponsors',
            name='access_token',
            field=models.CharField(default=bruc.models.generate_access_token, max_length=64, unique=True),
        ),
    ]
