# Generated by Django 2.2.7 on 2021-05-05 14:31

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cc_courses', '0047_auto_20210301_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
    ]
