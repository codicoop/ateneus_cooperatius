# Generated by Django 2.2.7 on 2020-08-06 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cc_courses', '0043_auto_20200805_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='activityenrolled',
            name='reminder_sent',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Recordatori enviat'),
        ),
    ]
