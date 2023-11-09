from django.db import migrations
from django.db.models import Q

from apps.coopolis.choices import CirclesChoices


def generate_created_entities(apps, schema_editor):
    print('')
    created_entities_model = apps.get_model("coopolis", "CreatedEntity")
    project_model = apps.get_model("coopolis", "Project")
    project_stage_model = apps.get_model("coopolis", "ProjectStage")

    projects = project_model.objects.filter().exclude(
        Q(cif__isnull=True)
        | Q(cif="")
        | Q(constitution_date__isnull=True)
        | Q(subsidy_period__isnull=True)
    )
    for project in projects:
        # Aquesta manera d'omplir les dades és exactament la que es feia servir
        # al seu moment per omplir les dades de l'excel, quan les dades de les
        # constituïdes es deduïen de les dades del propi projecte.
        service = None
        sub_service = None
        circle = None
        # The entity field is an exception to what said before. In the excel,
        # we were putting a string with all the involved entities in sessions
        # of the project's stage. Now, we need to fill a FK, so we're taking
        # the first entity of the first stage of the project.
        entity = None
        stages = project_stage_model.objects.filter(
            project=project,
            subsidy_period=project.subsidy_period,
        ).order_by("-date_start")[:1]
        if stages:
            stage = stages.all()[0]
            if stage.service:
                service = stage.service
            if stage.sub_service:
                sub_service = stage.sub_service
            if stage.circle:
                circle = CirclesChoices(stage.circle).value
            # There's the method ProjectStageSession.latest_session that
            # does exactly this, but we cannot use model methods when importing
            # with get_model().
            try:
                latest_session = stage.stage_sessions.latest("date")
            except:
                latest_session = None
            if latest_session:
                entity = latest_session.entity

        obj, created = created_entities_model.objects.update_or_create(
            project=project,
            defaults={
                "project": project,
                "service": service,
                "sub_service": sub_service,
                "subsidy_period": project.subsidy_period,
                "circle": circle,
                "entity": entity,
            },
        )
        print(f"Generat registre d'Entitat Creada pel projecte: {project.name}")


class Migration(migrations.Migration):

    dependencies = [
        ('coopolis', '0107_auto_20230919_1225'),
    ]

    operations = [
        migrations.RunPython(generate_created_entities),
    ]
