# Generated by Django 3.2.9 on 2021-11-08 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities_reservations', '0004_auto_20190923_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='room',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
