# Generated by Django 2.0.13 on 2019-08-02 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coopolis', '0019_auto_20190802_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectstage',
            name='hours',
            field=models.IntegerField(blank=True, help_text='Camp necessari per la justificació.', null=True, verbose_name="número d'hores"),
        ),
        migrations.AlterField(
            model_name='projectstage',
            name='stage_type',
            field=models.CharField(choices=[('1', '00 Nova creació - acollida'), ('2', '01 Nova creació - procés'), ('6', '02 Nova creació - constitució'), ('7', '03 Consolidació - 1a acollida'), ('8', '04 Consolidació - acompanyament')], default=1, max_length=2, verbose_name="tipus d'acompanyament"),
        ),
    ]
