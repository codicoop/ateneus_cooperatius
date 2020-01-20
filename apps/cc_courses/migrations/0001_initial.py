# Generated by Django 2.1.3 on 2019-03-11 19:59

import cc_courses.models
from django.db import migrations, models
import django.db.models.deletion
import easy_thumbnails.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='títol')),
                ('objectives', models.TextField(null=True, verbose_name='descripció')),
                ('date_start', models.DateField(verbose_name='dia inici')),
                ('date_end', models.DateField(blank=True, null=True, verbose_name='dia finalització')),
                ('starting_time', models.TimeField(verbose_name="hora d'inici")),
                ('ending_time', models.TimeField(verbose_name='hora de finalització')),
                ('spots', models.IntegerField(default=0, verbose_name='places totals')),
                ('axis', models.CharField(blank=True, choices=[('B', 'Eix B'), ('C', 'Eix C'), ('D', 'Eix D')], help_text='Eix de la convocatòria on es justificarà.', max_length=1, null=True, verbose_name='eix')),
                ('published', models.BooleanField(default=True, verbose_name='publicada')),
            ],
            options={
                'verbose_name': 'activitat',
                'ordering': ['-date_start'],
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='títol')),
                ('slug', models.CharField(max_length=250, unique=True)),
                ('date_start', models.DateField(verbose_name='dia inici')),
                ('date_end', models.DateField(blank=True, null=True, verbose_name='dia finalització')),
                ('hours', models.CharField(help_text='Indica només els horaris, sense els dies.', max_length=200, verbose_name='horaris')),
                ('description', models.TextField(null=True, verbose_name='descripció')),
                ('published', models.BooleanField(verbose_name='publicat')),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('banner', easy_thumbnails.fields.ThumbnailerImageField(max_length=250, null=True)),
            ],
            options={
                'verbose_name': 'formació',
                'verbose_name_plural': 'formacions',
                'ordering': ['-date_start'],
            },
        ),
        migrations.CreateModel(
            name='CoursePlace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='nom')),
                ('address', models.CharField(max_length=200, verbose_name='adreça')),
            ],
            options={
                'verbose_name': 'lloc',
            },
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='nom')),
                ('legal_id', models.CharField(default='G66622002', max_length=9, verbose_name='N.I.F.')),
            ],
            options={
                'verbose_name': 'entitat',
            },
        ),
        migrations.AddField(
            model_name='activity',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cc_courses.Course', verbose_name='formació / programa'),
        ),
    ]
