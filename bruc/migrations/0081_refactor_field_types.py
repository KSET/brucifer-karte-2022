from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('bruc', '0080_data_migration_pre_refactor'),
    ]

    operations = [
        # Guests
        migrations.AlterField(
            model_name='guests',
            name='bought',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='guests',
            name='entered',
            field=models.BooleanField(default=False),
        ),
        # Tags
        migrations.AlterField(
            model_name='tags',
            name='count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tags',
            name='bought',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tags',
            name='entered',
            field=models.IntegerField(default=0),
        ),
        # Sponsors
        migrations.AlterField(
            model_name='sponsors',
            name='guestsEnabled',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='sponsors',
            name='guestCap',
            field=models.IntegerField(null=True, blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='sponsors',
            name='order',
            field=models.IntegerField(default=0),
        ),
        # Cjenik
        migrations.AlterField(
            model_name='cjenik',
            name='priceEUR',
            field=models.DecimalField(max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AlterField(
            model_name='cjenik',
            name='volume',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='cjenik',
            name='order',
            field=models.IntegerField(default=0),
        ),
        # Visibility
        migrations.AlterField(
            model_name='visibility',
            name='visible',
            field=models.BooleanField(default=False),
        ),
        # GameLeaderboard
        migrations.AlterField(
            model_name='gameleaderboard',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]
