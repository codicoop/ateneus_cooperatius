# Generated by Django 3.2.14 on 2022-07-06 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cc_courses', '0058_alter_activity_sub_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Si la desactives no apareixerà al desplegable.', verbose_name='Activa'),
        ),
    ]
