# Generated by Django 2.0 on 2019-09-23 10:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cc_courses', '0022_activity_subaxis'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='títol')),
                ('start', models.DateTimeField(verbose_name="data i hora d'inici")),
                ('end', models.DateTimeField(verbose_name='data i hora de finalització')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creació')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='creat per…')),
                ('responsible', models.ForeignKey(blank=True, help_text="Persona de l'equip al càrrec de la reserva. Per aparèixer al desplegable, cal que la persona tingui activada la opció 'Membre del personal'.", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reservations', to=settings.AUTH_USER_MODEL, verbose_name='persona responsable')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cc_courses.CoursePlace', verbose_name='sala')),
            ],
            options={
                'verbose_name': 'reserva',
                'verbose_name_plural': 'reserves',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='nom')),
                ('color', models.CharField(default='#e94e1b', max_length=7, verbose_name='color al calendari')),
                ('capacity', models.IntegerField(blank=True, default=None, null=True, verbose_name='capacitat')),
                ('place', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cc_courses.CoursePlace', verbose_name='lloc')),
            ],
            options={
                'verbose_name': 'sala',
                'verbose_name_plural': 'sales',
            },
        ),
    ]
