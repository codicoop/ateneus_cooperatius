# Generated by Django 2.1.3 on 2019-04-10 18:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cc_courses', '0007_auto_20190410_1847'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activity',
            old_name='published',
            new_name='publish',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='published',
            new_name='publish',
        ),
    ]
