# Generated by Django 2.1.3 on 2019-07-29 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coopolis', '0017_auto_20190724_1621'),
        ('cc_courses', '0020_auto_20190604_2004'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseplace',
            name='town',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='coopolis.Town', verbose_name='població'),
        ),
    ]
