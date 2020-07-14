# Generated by Django 2.2.7 on 2020-07-14 15:04

import coopolis.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coopolis', '0060_auto_20200616_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='estatuts',
            field=models.FileField(blank=True, max_length=250, null=True, storage=coopolis.storage_backends.PrivateMediaStorage(), upload_to='', verbose_name='estatuts'),
        ),
        migrations.AlterField(
            model_name='project',
            name='sostenibility',
            field=models.FileField(blank=True, max_length=250, null=True, storage=coopolis.storage_backends.PrivateMediaStorage(), upload_to='', verbose_name='pla de sostenibilitat'),
        ),
        migrations.AlterField(
            model_name='project',
            name='viability',
            field=models.FileField(blank=True, max_length=250, null=True, storage=coopolis.storage_backends.PrivateMediaStorage(), upload_to='', verbose_name='pla de viabilitat'),
        ),
        migrations.AlterField(
            model_name='projectstage',
            name='scanned_certificate',
            field=models.FileField(blank=True, max_length=250, null=True, storage=coopolis.storage_backends.PrivateMediaStorage(), upload_to='', verbose_name='certificat'),
        ),
        migrations.AlterField(
            model_name='projectstage',
            name='scanned_signatures',
            field=models.FileField(blank=True, max_length=250, null=True, storage=coopolis.storage_backends.PrivateMediaStorage(), upload_to='', verbose_name='fitxa de projectes (document amb signatures)'),
        ),
    ]
