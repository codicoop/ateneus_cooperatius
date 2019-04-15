# Generated by Django 2.1.3 on 2019-04-15 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coopolis', '0004_auto_20190415_1351'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectstage',
            options={'ordering': ['-date_start'], 'verbose_name': "justificació d'acompanyament", 'verbose_name_plural': "justificacions d'acompanyaments"},
        ),
        migrations.AlterField(
            model_name='projectstage',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coopolis.Project', verbose_name='projecte acompanyat'),
        ),
    ]
