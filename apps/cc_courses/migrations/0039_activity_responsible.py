# Generated by Django 2.2.7 on 2020-07-09 14:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cc_courses', '0038_remove_activity_justification'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='responsible',
            field=models.ForeignKey(blank=True, help_text="Persona de l'equip al càrrec de la sessió. Per aparèixer al desplegable, cal que la persona tingui activada la opció 'Membre del personal'.", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activities_responsible', to=settings.AUTH_USER_MODEL, verbose_name='persona responsable'),
        ),
    ]
