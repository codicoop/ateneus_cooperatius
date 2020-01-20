# Generated by Django 2.1.3 on 2019-06-03 11:02

import coopolis.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coopolis', '0008_auto_20190531_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectstage',
            name='scanned_certificate',
            field=models.FileField(blank=True, max_length=250, null=True, verbose_name='certificat'),
        ),
        migrations.AlterField(
            model_name='projectstage',
            name='axis',
            field=models.CharField(blank=True, choices=[('A', 'Eix A'), ('B', 'Eix B'), ('C', 'Eix C'), ('D', 'Eix D'), ('E', 'Eix E'), ('F', 'Eix F')], help_text='Eix de la convocatòria on es justificarà.', max_length=1, null=True, verbose_name='eix'),
        ),
        migrations.AlterField(
            model_name='projectstage',
            name='scanned_signatures',
            field=models.FileField(blank=True, max_length=250, null=True, verbose_name='fitxa de projectes (document amb signatures)'),
        ),
    ]
