# Generated by Django 3.2.14 on 2024-02-21 09:41

import apps.coopolis.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coopolis', '0112_auto_20240220_1141'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='photo',
            field=models.FileField(blank=True, max_length=250, null=True, storage=apps.coopolis.storage_backends.PrivateMediaStorage(), upload_to='', verbose_name='fotografia'),
        ),
    ]
