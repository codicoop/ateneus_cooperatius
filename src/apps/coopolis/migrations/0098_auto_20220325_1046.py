# Generated by Django 3.2.9 on 2022-03-25 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coopolis', '0097_datamigration_mail_project_confirm'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='derivation',
            options={'ordering': ['name'], 'verbose_name': 'derivació', 'verbose_name_plural': 'derivacions'},
        ),
        migrations.AlterModelOptions(
            name='town',
            options={'ordering': ['name'], 'verbose_name': 'població', 'verbose_name_plural': 'poblacions'},
        ),
        migrations.AlterField(
            model_name='activitypoll',
            name='met_new_people',
            field=models.BooleanField(null=True, verbose_name="M'ha permès conèixer persones afins"),
        ),
        migrations.AlterField(
            model_name='activitypoll',
            name='wanted_start_cooperative',
            field=models.BooleanField(null=True, verbose_name="Abans del curs, teníeu ganes/necessitats d'engegar algun projecte cooperatiu"),
        ),
        migrations.AlterField(
            model_name='activitypoll',
            name='wants_start_cooperative_now',
            field=models.BooleanField(null=True, verbose_name='I després?'),
        ),
        migrations.AlterField(
            model_name='project',
            name='sector',
            field=models.CharField(choices=[('M', 'Alimentació'), ('S', 'Assessorament'), ('A', 'Altres'), ('C', 'Comunicació i tecnologia'), ('CU', 'Cultura'), ('U', 'Cures'), ('E', 'Educació'), ('F', 'Finances'), ('H', 'Habitatge'), ('L', 'Logística'), ('O', 'Oci'), ('R', 'Roba')], max_length=2),
        ),
    ]
