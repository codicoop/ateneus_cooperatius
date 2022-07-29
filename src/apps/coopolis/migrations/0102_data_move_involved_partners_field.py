from django.db import migrations


def move_involved_partners_field(apps, schema_editor):
    """
    Fins ara durant l'acompanyament de projectes es donava d'alta un
    Acompanyament al que s'hi indicàven les persones sòcies que hi participen,
    de manera que a la justificació, hi posàvem totes les persones de tots els
    acompanyaments que s'hagin fet a cada projecte.

    Degut a que durant les diverses sessions que es fan durant l'acompanyament
    hi participen diferents persones, es feia complicat mantenir la relació de
    persones totals fent servir el camp dins del propi acompanyament.

    Per això ara el camp es mou d'Acompanyament -> Sessió d'Acompanyament, així
    a cada sessió s'hi indicarà les persones.

    Per tant també es modifica la justificació de manera que ara reculli totes
    les persones de totes les sessions de tots els acompanyaments de cada
    projecte.

    Aquesta migració trasllada totes les persones participants d'un
    acompanyament cap a la primera sessió que trobi.
    Davant de la possibilitat que un acompanyament no tingui cap sessió,
    prèviament s'ha fet un procés de verificar si es dona algun cas, i s'ha
    confirmat que sí que hi ha casos en que això passa.
    En aquests casos, si hi ha participants a l'acompanyyament, es crea una
    sessió per poder-los-hi migrar.
    """
    print('')
    projectstage_model = apps.get_model("coopolis", "ProjectStage")
    stagesession_model = apps.get_model("coopolis", "ProjectStageSession")

    project_stages = projectstage_model.objects.filter(
        involved_partners__isnull=False,
    )
    for project_stage in project_stages:
        try:
            stage_session = project_stage.stage_sessions.all()[0]
        except IndexError:
            # This stage does not have any session, we create it now
            stage_session = stagesession_model(
                project_stage=project_stage,
                date=project_stage.date_start,
                follow_up="[sessió creada automàticament per poder moure els "
                "participants que abans es desaven a la fitxa de "
                "l'acompanyament i eventualment es van eliminar d'allà i "
                "traslladar a aquesta sessió d'acompanyament]",
            )
            stage_session.clean()
            stage_session.save()
        stage_session.involved_partners.add(
            *project_stage.involved_partners.all()
        )
        # At this point we don't delete the project_stage.involved_partners
        # so we can verify the information at any time, and we will delete the
        # field altogether in next iterations.
    print("Participants dels acompanyaments moguts cap a la 1a sessió "
          "d'acompanyament.")


class Migration(migrations.Migration):

    dependencies = [
        ("coopolis", "0101_auto_20220729_1823"),
    ]

    operations = [
        migrations.RunPython(move_involved_partners_field),
    ]
