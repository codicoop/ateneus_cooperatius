# Generated by Django 2.2.7 on 2020-09-15 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataexports', '0015_datamigration_cofunded_and_descriptions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dataexports',
            options={'ordering': ['subsidy_period'], 'verbose_name': 'exportació', 'verbose_name_plural': 'exportacions'},
        ),
    ]
