# Generated by Django 2.2.7 on 2020-01-20 12:38

from django.contrib.postgres.operations import UnaccentExtension
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coopolis', '0035_subsidy_period_to_fk'),
    ]

    operations = [
        UnaccentExtension(),
    ]
