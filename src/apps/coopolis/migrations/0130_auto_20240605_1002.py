# Generated by Django 3.2.14 on 2024-06-05 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coopolis', '0129_data_sta_ma_corco'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createdentity',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_entities', to='coopolis.project', verbose_name='(Obsolet) Projecte'),
        ),
        migrations.AlterField(
            model_name='project',
            name='follow_up_situation',
            field=models.CharField(blank=True, choices=[('PENDENT', 'Pendent d’enviar proposta de trobada'), ('ENVIAT', 'Enviat email amb proposta de data per trobar-nos'), ('CONCERTADA', 'Data de trobada concertada'), ('ACOLLIT', 'Acollida realitzada'), ('EN_CURS', 'Acompanyament en curs'), ('PAUSA', 'Acompanyament en pausa'), ('CANCEL', 'Acompanyament cancel·lat')], max_length=50, null=True, verbose_name='seguiment'),
        ),
        migrations.AlterField(
            model_name='user',
            name='cannot_share_id',
            field=models.BooleanField(default=False, verbose_name='Obsolet'),
        ),
    ]
