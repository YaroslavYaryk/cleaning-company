# Generated by Django 4.1 on 2022-08-17 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('picture', models.ImageField(blank=True, upload_to='images/users')),
                ('phone', models.CharField(blank=True, max_length=50)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('personal_number', models.IntegerField()),
                ('account_number', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
