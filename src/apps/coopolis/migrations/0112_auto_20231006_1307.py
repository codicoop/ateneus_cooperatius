# Generated by Django 3.2.14 on 2023-10-06 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coopolis', '0111_auto_20231005_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectstage',
            name='exclude_from_justification',
            field=models.BooleanField(default=False, verbose_name="No incloure a l'excel de justificació"),
        ),
        migrations.AlterField(
            model_name='town',
            name='name_for_justification',
            field=models.CharField(blank=True, default='', max_length=250, verbose_name='nom per la justificació'),
        ),
    ]
