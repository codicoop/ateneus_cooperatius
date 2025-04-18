# Generated by Django 2.2.7 on 2020-01-22 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coopolis', '0040_auto_20200122_1000'),
    ]

    operations = [
        migrations.CreateModel(
            name='StagesByAxis',
            fields=[
            ],
            options={
                'verbose_name': 'acompanyament',
                'verbose_name_plural': 'Acompanyaments per Eix',
                'ordering': ['axis', 'subaxis', 'organizer', 'date_start'],
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('coopolis.projectstage',),
        ),
    ]
