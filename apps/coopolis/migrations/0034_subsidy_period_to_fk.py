# Generated by Django 2.2.7 on 2020-01-17 14:51

from django.db import migrations


def subsidy_period_migration(apps, schema_editor):
    projectstage = apps.get_model('coopolis', 'ProjectStage')
    SubsidyPeriod = apps.get_model('dataexports', 'SubsidyPeriod')
    for obj in projectstage.objects.all():
        starting_year = int(obj.subsidy_period) - 1
        subsidyperiod = SubsidyPeriod.objects.get(name__startswith=starting_year)
        obj.subsidy_period_link = subsidyperiod
        obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('coopolis', '0033_projectstage_subsidy_period_link'),
    ]

    operations = [
        migrations.RunPython(subsidy_period_migration),
    ]
