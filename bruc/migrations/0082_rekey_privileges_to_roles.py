from django.db import migrations, models


# Old integer-string privilege -> new role-key string.
FORWARD_MAP = {
    "0": "none",
    "1": "admin",
    "2": "entry",
    "3": "tickets",
    "4": "entry_tickets",
}
REVERSE_MAP = {v: k for k, v in FORWARD_MAP.items()}


def rekey_forward(apps, schema_editor):
    Users = apps.get_model("bruc", "Users")
    valid_keys = set(FORWARD_MAP.values())
    for user in Users.objects.all():
        # Unknown/empty values fall back to "none" (fail-closed).
        if user.privilege in valid_keys:
            continue
        new_value = FORWARD_MAP.get(user.privilege, "none")
        if new_value != user.privilege:
            user.privilege = new_value
            user.save(update_fields=["privilege"])


def rekey_reverse(apps, schema_editor):
    Users = apps.get_model("bruc", "Users")
    for user in Users.objects.all():
        old_value = REVERSE_MAP.get(user.privilege)
        if old_value is not None and old_value != user.privilege:
            user.privilege = old_value
            user.save(update_fields=["privilege"])


class Migration(migrations.Migration):

    dependencies = [
        ("bruc", "0081_refactor_field_types"),
    ]

    operations = [
        migrations.AlterField(
            model_name="users",
            name="privilege",
            field=models.CharField(
                choices=[
                    ("none", "Ništa"),
                    ("admin", "Admin"),
                    ("entry", "Ulaz"),
                    ("tickets", "Karte"),
                    ("entry_tickets", "Ulaz+Karte"),
                ],
                default="none",
                max_length=50,
            ),
        ),
        migrations.RunPython(rekey_forward, rekey_reverse),
    ]
