# Generated by Django 2.2.7 on 2021-03-02 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coopolis', '0078_covid_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cannot_share_id',
            field=models.BooleanField(default=False, help_text="Si degut a la teva situació legal et suposa un inconvenient indicar el DNI, deixa'l en blanc i marca aquesta casella"),
        ),
    ]
