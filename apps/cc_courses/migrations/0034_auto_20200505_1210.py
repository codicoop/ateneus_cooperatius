# Generated by Django 2.2.7 on 2020-05-05 10:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cc_courses', '0033_auto_20200407_1330'),
    ]

    operations = [
        migrations.AddField(
            model_name='activityenrolled',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activityenrolled',
            name='waiting_list',
            field=models.BooleanField(default=False, verbose_name="en llista d'espera"),
            preserve_default=False,
        ),
    ]
