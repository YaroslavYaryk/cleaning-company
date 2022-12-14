# Generated by Django 4.1 on 2022-09-01 04:35

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("worker", "0004_workershift_date"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="workershift",
            unique_together={("user", "shift", "date")},
        ),
    ]
