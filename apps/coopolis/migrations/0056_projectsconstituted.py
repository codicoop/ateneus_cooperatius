# Generated by Django 2.2.7 on 2020-06-10 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coopolis', '0055_auto_20200610_1342'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectsConstituted',
            fields=[
            ],
            options={
                'verbose_name': 'Projecte constituït',
                'verbose_name_plural': 'Projectes constituïts',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('coopolis.project',),
        ),
    ]
