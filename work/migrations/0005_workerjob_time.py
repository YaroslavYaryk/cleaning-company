# Generated by Django 4.1 on 2022-09-20 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("work", "0004_rename_room_work_work_worker_job"),
    ]

    operations = [
        migrations.AddField(
            model_name="workerjob",
            name="time",
            field=models.TimeField(null=True),
        ),
    ]
