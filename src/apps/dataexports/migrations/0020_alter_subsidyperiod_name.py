# Generated by Django 3.2.9 on 2021-11-08 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataexports', '0019_auto_20211108_0936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subsidyperiod',
            name='name',
            field=models.CharField(max_length=250, unique=True, verbose_name='nom'),
        ),
    ]
