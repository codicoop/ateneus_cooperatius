# Generated by Django 2.2.7 on 2020-08-03 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cc_courses', '0042_auto_20200717_1041'),
        ('coopolis', '0064_auto_20200717_0958'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectstage',
            name='cofunded',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cofunded_projects', to='cc_courses.Cofunding', verbose_name='Cofinançat'),
        ),
        migrations.AddField(
            model_name='projectstage',
            name='cofunded_ateneu',
            field=models.BooleanField(default=False, verbose_name='Cofinançat amb Ateneus Cooperatius'),
        ),
        migrations.AddField(
            model_name='projectstage',
            name='strategic_line',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='strategic_line_projects', to='cc_courses.StrategicLine', verbose_name='línia estratègica'),
        ),
    ]
