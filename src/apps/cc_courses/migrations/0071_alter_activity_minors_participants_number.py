# Generated by Django 3.2.14 on 2024-11-25 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cc_courses', '0070_merge_20240424_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='minors_participants_number',
            field=models.IntegerField(blank=True, default=0, verbose_name="número d'alumnes participants"),
        ),
    ]
