# Generated by Django 3.2.14 on 2024-06-06 09:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cc_courses', '0070_merge_20240424_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='date_end',
            field=models.DateField(default=datetime.date(2024, 6, 6), verbose_name='dia finalització'),
        ),
    ]
