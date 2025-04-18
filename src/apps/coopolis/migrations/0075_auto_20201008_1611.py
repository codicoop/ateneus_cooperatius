# Generated by Django 2.2.7 on 2020-10-08 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coopolis', '0074_datamigr_clean_contract_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employmentinsertion',
            name='duration',
        ),
        migrations.AlterField(
            model_name='employmentinsertion',
            name='contract_type',
            field=models.SmallIntegerField(choices=[(1, 'Indefinit'), (2, 'Formació i aprenentatge'), (3, 'Pràctiques'), (4, 'Soci/a cooperativa o societat laboral')], null=True, verbose_name='tipus de contracte'),
        ),
    ]
