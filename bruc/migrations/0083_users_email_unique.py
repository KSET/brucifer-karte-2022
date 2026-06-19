from collections import defaultdict

from django.db import migrations, models
from django.db.models import Q


ROLE_RANK = {
    "admin": 5,
    "entry_tickets": 4,
    "tickets": 3,
    "entry": 2,
    "none": 1,
}


def dedupe_emails(apps, schema_editor):
    Users = apps.get_model("bruc", "Users")
    groups = defaultdict(list)
    for u in Users.objects.exclude(email="").only("id", "email", "privilege"):
        groups[u.email].append(u)
    for email, rows in groups.items():
        if len(rows) < 2:
            continue
        rows.sort(key=lambda r: (-ROLE_RANK.get(r.privilege, 0), r.id))
        for dup in rows[1:]:
            dup.delete()


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("bruc", "0082_rekey_privileges_to_roles"),
    ]

    operations = [
        migrations.RunPython(dedupe_emails, noop_reverse),
        migrations.AlterField(
            model_name="users",
            name="email",
            field=models.EmailField(blank=True, default="", max_length=254),
        ),
        migrations.AddConstraint(
            model_name="users",
            constraint=models.UniqueConstraint(
                condition=~Q(email=""),
                fields=("email",),
                name="uniq_users_email_nonblank",
            ),
        ),
    ]
