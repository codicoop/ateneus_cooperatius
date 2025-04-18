# Generated by Django 3.2.14 on 2024-04-19 14:28

import apps.coopolis.storage_backends
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coopolis', '0122_auto_20240415_1554'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(help_text="Mides aprox: 400px d'amplada x 200px d'alçada. Idealment, fons transparent.", null=True, storage=apps.coopolis.storage_backends.PublicMediaStorage(), upload_to='', verbose_name='Logotip')),
                ('signatures_pdf_footer', models.ImageField(help_text="Mides: 1.241px d'amplada x 280px d'alçada. Fons blanc.", null=True, storage=apps.coopolis.storage_backends.PublicMediaStorage(), upload_to='', verbose_name='Imatge del peu de pàgina de signatures')),
            ],
            options={
                'verbose_name': "Configuració de l'aplicació",
                'verbose_name_plural': "Configuració de l'aplicació",
            },
        ),
        migrations.AlterField(
            model_name='createdentity',
            name='project_stage',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_entity', to='coopolis.projectstage', verbose_name="Acompanyament vinculat a la creació de l'entitat"),
        ),
    ]
