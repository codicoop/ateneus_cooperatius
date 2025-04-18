# Generated by Django 2.2.7 on 2020-06-10 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coopolis', '0054_auto_20200610_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='employment_estimation',
            field=models.PositiveIntegerField(default=0, verbose_name='insercions laborals previstes'),
        ),
        migrations.AlterField(
            model_name='project',
            name='other',
            field=models.CharField(blank=True, help_text="Apareix a la taula de Seguiment d'Acompanyaments", max_length=240, null=True, verbose_name='altres'),
        ),
    ]
