# Generated by Django 4.1 on 2022-08-27 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("work", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="work",
            name="room_work",
        ),
        migrations.AddField(
            model_name="work",
            name="room_work",
            field=models.ManyToManyField(to="work.roomwork", verbose_name="room_work"),
        ),
    ]
