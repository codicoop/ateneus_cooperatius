# Generated by Django 2.1.3 on 2019-07-24 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coopolis', '0013_auto_20190724_1306'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProjectStageType',
        ),
        migrations.AlterField(
            model_name='projectstage',
            name='stage_type',
            field=models.CharField(choices=[('1', '00 Acollida'), ('2', '01 Procés'), ('6', '02 Constitució'), ('7', '03 Consolidació - 1a acollida'), ('8', '04 Consolidació - acompanyament')], default=1, max_length=2, verbose_name="tipus d'acompanyament"),
        ),
    ]
