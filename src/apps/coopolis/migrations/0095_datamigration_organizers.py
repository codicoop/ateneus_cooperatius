# Generated by Django 3.2.9 on 2022-01-04 09:10
from django.conf import settings
from django.db import migrations
from django.db.models import F

from apps.coopolis.choices import CirclesChoices


def migrate_organizer_to_circle(apps, schema_editor):
    # Disabled for safety. For instance, we're not using anymore the
    # settings.PROJECT_NAME var, so it would not work anyway, and once this
    # migration was done, it's not needed anymore, specially not in new
    # deployments.
    return
    """
    This migration comes out of the necessity for normnalizing the information
    in:
    - entity and organizer fields in Activity
    - stage_organizer in ProjectStage and ProjectStageSession.entity.

    Organizer was supposed to contain the different circles, but with the mix
    of some mistakes from Codi and some ateneus, nowadays some ateneus have
    the circles stored in the entity field instead.

    We created a new field 'circle' which is a choices instead of a foreignkey
    field, and this migration's purpose is to fill this field with the right
    organizer/entity information.
    """
    activity_model = apps.get_model('cc_courses', 'Activity')
    stage_model = apps.get_model('coopolis', 'ProjectStage')
    stagesession_model = apps.get_model('coopolis', 'ProjectStageSession')
    organizer_model = apps.get_model('cc_courses', 'Organizer')
    entity_model = apps.get_model('cc_courses', 'Entity')
    print("settings.PROJECT_NAME: " + settings.PROJECT_NAME)
    if "Alt Pirineu" in settings.PROJECT_NAME:
        migrate_altpirineu(
            activity_model,
            stage_model,
            organizer_model,
            entity_model,
            stagesession_model,
        )
    elif "Catalunya Central" in settings.PROJECT_NAME:
        migrate_catcentral(
            activity_model,
            stage_model,
            organizer_model,
            entity_model,
            stagesession_model,
        )
    elif "Coopcamp" in settings.PROJECT_NAME:
        migrate_coopcamp(
            activity_model,
            stage_model,
            organizer_model,
            entity_model,
            stagesession_model,
        )
    elif "Coopmaresme" in settings.PROJECT_NAME:
        migrate_coopmaresme(
            activity_model,
            stage_model,
            organizer_model,
            entity_model,
            stagesession_model,
        )
    elif "Coòpolis" in settings.PROJECT_NAME:
        migrate_coopolis(
            activity_model,
            stage_model,
            organizer_model,
            entity_model,
            stagesession_model,
        )
    elif "Coopsetània" in settings.PROJECT_NAME:
        migrate_coopsetania(
            activity_model,
            stage_model,
            organizer_model,
            entity_model,
            stagesession_model,
        )
    elif "La Col·lectiva" in settings.PROJECT_NAME:
        migrate_hospitalet(
            activity_model,
            stage_model,
            organizer_model,
            entity_model,
            stagesession_model,
        )
    elif "Ponent Coopera" in settings.PROJECT_NAME:
        migrate_ponentcoopera(
            activity_model,
            stage_model,
            organizer_model,
            entity_model,
            stagesession_model,
        )
    elif "Terres de l'Ebre" in settings.PROJECT_NAME:
        migrate_terresebre(
            activity_model,
            stage_model,
            organizer_model,
            entity_model,
            stagesession_model,
        )
    elif "Terres Gironines" in settings.PROJECT_NAME:
        migrate_terresgironines(
            activity_model,
            stage_model,
            organizer_model,
            entity_model,
            stagesession_model,
        )
    elif "Vallès Occidental" in settings.PROJECT_NAME:
        migrate_vallesoccidental(
            activity_model,
            stage_model,
            organizer_model,
            entity_model,
            stagesession_model,
        )


def migrate_altpirineu(
            activity_model,
            stage_model,
            organizer_model,
            entity_model,
            stagesession_model,
        ):
    """
    La dada d'ateneu/cercle la tenen al camp Entitat, tot i que només tenen
    l'Ateneu.
    L'entitat es diu ATENEU COOPERATIU DE L'ALT PIRINEU I ARAN.

    A Organizer hi tenen consells comarcals i el propi ateneu, cosa que serien
    les entitats, per tant caldria moure-ho a Entity.

    Caldria:
    - assignar totes les Activity i ProjectStage al circle.CERCLE0
    - assignar totes les Activity.entity i ProjectStageSession.entity a None.
    - eliminar tots (l'únic) registre d'Entity.
    - copiar tots els Organizer cap a Entity.
    - per cada Activity, assignar Activity.entity = Activity.organizer.
    - per cada ProjectStage, assignar a tots els
      seus ProjectStageSession.entity = ProjectStage.stage_organizer.
    - eliminar tots els registres d'Organizer.
    """
    print("REORGANITZANT CERCLES PER ALT PIRINEU I ARAN")
    print("assignar totes les Activity.organizer al circle.CERCLE0"
          "i totes les Activity.entity a None")
    updated = activity_model.objects.all().update(
        circle=CirclesChoices.CERCLE0,
        entity=None,
    )
    print(f"{updated} registres actualitzats.")
    print("assignar totes les Activity.entity a None.")
    updated = stagesession_model.objects.all().update(
        entity=None,
    )
    print(f"{updated} registres actualitzats.")
    print("assignar totes les ProjectStageSession.entity a None.")
    updated = stage_model.objects.all().update(
        circle=CirclesChoices.CERCLE0,
    )
    print(f"{updated} registres actualitzats.")
    print("eliminar tots (l'únic) registre d'Entity.")
    entity_model.objects.all().delete()
    print("copiar tots els Organizer cap a Entity.")
    for organizer in organizer_model.objects.all():
        entity = entity_model(id=organizer.id, name=organizer.name)
        entity.save()
    print("per cada Activity, assignar Activity.entity = Activity.organizer.")
    for activity in activity_model.objects.all():
        if not activity.organizer:
            continue
        activity.entity_id = activity.organizer.id
        activity.save()
    print("per cada ProjectStage, assignar a tots els "
          "seus ProjectStageSession.entity = ProjectStage.stage_organizer.")
    for stage in stage_model.objects.all():
        stage.stage_sessions.all().update(
            entity=stage.stage_organizer,
        )
    print("eliminar tots els registres d'Organizer.")
    organizer_model.objects.all().delete()


def migrate_catcentral(
            activity_model,
            stage_model,
            organizer_model,
            entity_model,
            stagesession_model,
        ):
    """
    A Organizer hi tenen 2 registres però que no han fet servir ni a Activity
    ni a ProjectStage. Per tant es pot eliminar.

    A Entity hi tenen els ateneu/cercles, però l'única que han fet servir a les
    Activity i a les ProjectStageSession és l'Ateneu.

    Caldria:
    - assignar totes les Activity.circle al circle.CERCLE0,
          totes les Activity.entity a None i totes les Activity.organizer
          a None
    - assignar totes ProjectStage.circle al circle.CERCLE0 i ProjectStage.stage_organizer a None

    - assignar totes les ProjectStageSession.entity a None.
    - eliminar tots els registres d'Entity.
    - eliminar totes els registres d'Organizer.
    """
    print("REORGANITZANT CERCLES PER CATALUNYA CENTRAL")
    print("assignar totes les Activity.circle al circle.CERCLE0,"
          "totes les Activity.entity a None i totes les Activity.organizer"
          "a None")
    updated = activity_model.objects.all().update(
        circle=CirclesChoices.CERCLE0,
        entity=None,
        organizer=None,
    )
    print(f"{updated} registres actualitzats.")
    print("assignar tots els ProjectStage.circle al CERCLE0")
    updated = stage_model.objects.all().update(
        circle=CirclesChoices.CERCLE0,
        stage_organizer=None,
    )
    print(f"{updated} registres actualitzats.")
    print("assignar totes les ProjectStageSession.entity a None")
    updated = stagesession_model.objects.all().update(
        entity=None,
    )
    print(f"{updated} registres actualitzats.")
    print("eliminar tots els registres d'Entity")
    entity_model.objects.all().delete()
    print("eliminar tots els registres d'Organizer.")
    organizer_model.objects.all().delete()


def migrate_coopcamp(
            activity_model,
            stage_model,
            organizer_model,
            entity_model,
            stagesession_model,
        ):
    """
    Els noms i IDs dels Organizers son:
    Ateneu=1
    CIRCLE_NAME_1=Agroecològic=4
    CIRCLE_NAME_2=Vulnerabilitats= NO té ID, no existia abans.
    CIRCLE_NAME_3=Tarragonès=3
    CIRCLE_NAME_4=Reus=5
    CIRCLE_NAME_5=Baix Penedès=2

    NOTA: CERCLE2 abans era Baix Penedès. M'han informat que s'elimina així que
    l'hem mogut al 5 com a forma fàcil de fer-lo obsolet.
    Això implica tornar a tirar la migració a develop i tornar de manar que
    donin l'OK a les dades.
    En un futur caldrà trobar una manera de poder desactivar cercles mantenint
    l'històric.

    Entitat ho tenen correcte.

    Cal:
    - per cada Activity, posar Activity.circle corresponent a Activity.organizer
    - posar totes les Activity.organizer a None
    - Organizer.delete()
    """
    print("REORGANITZANT CERCLES PER COOPCAMP")
    print("Assignant Activity.circle segons l'Activity.organizer corresponent")
    circles = {
        1: CirclesChoices.CERCLE0,
        4: CirclesChoices.CERCLE1,
        2: CirclesChoices.CERCLE5,  # Was 2, now is 5 to deprecate Baix Penedès.
        3: CirclesChoices.CERCLE3,
        5: CirclesChoices.CERCLE4,
    }
    for organizer_id, circle in circles.items():
        updated = activity_model.objects.filter(organizer=organizer_id).update(
            circle=circle,
        )
        print(f"Activity actualitzats per organizer {organizer_id}: {updated}")
        updated = stage_model.objects.filter(stage_organizer=organizer_id).update(
            circle=circle,
        )
        print(f"ProjectStage actualitzats per organizer {organizer_id}: {updated}")
    print(f"Registres actualitzats: {updated}")
    print("Establint tots els Activity.organizer a None")
    updated = activity_model.objects.all().update(organizer=None)
    print(f"Registres actualitzats: {updated}")
    print("Establint tots els ProjectStage.stage_organizer a None")
    updated = stage_model.objects.all().update(stage_organizer=None)
    print(f"Registres actualitzats: {updated}")
    print("Eliminant tots els Organizers")
    organizer_model.objects.all().delete()


def migrate_coopmaresme(
            activity_model,
            stage_model,
            organizer_model,
            entity_model,
            stagesession_model,
        ):
    """
    Coopmaresme ho tenen bé i únicament una organitzadora, el propi ateneu.

    Cal:
    - per cada Activity, posar Activity.circle a CERCLE0
    - posar totes les Activity.organizer a None
    - Organizer.delete()
    """
    print("REORGANITZANT CERCLES PER COOPMARESME")
    print("Assignant Activity.circle a CIRCLE0")
    updated = activity_model.objects.all().update(
        circle=CirclesChoices.CERCLE0,
    )
    print(f"Registres actualitzats: {updated}")
    print("Establint tots els Activity.organizer a None")
    updated = activity_model.objects.all().update(organizer=None)
    print(f"Registres actualitzats: {updated}")
    print("assignar tots els ProjectStage.circle al CERCLE0")
    updated = stage_model.objects.all().update(
        circle=CirclesChoices.CERCLE0,
        stage_organizer=None,
    )
    print(f"{updated} registres actualitzats.")
    print("Eliminant tots els Organizers")
    organizer_model.objects.all().delete()


def migrate_coopolis(
            activity_model,
            stage_model,
            organizer_model,
            entity_model,
            stagesession_model,
        ):
    """
    Els noms i IDs dels Organizers son:
    Ateneu=5
    CIRCLE_NAME_1=Consum i Transició Agroecològica=4
    CIRCLE_NAME_2=Economies Feministes=7
    CIRCLE_NAME_3=Incubació - Coòpolis=3
    CIRCLE_NAME_4=Migracions - Coòpolis=2
    CIRCLE_NAME_5=Transició Ecosocial=6

    Entitat ho tenen correcte.

    Cal:
    - per cada Activity, posar Activity.circle corresponent a Activity.organizer
    - posar totes les Activity.organizer a None
    - Organizer.delete()
    """
    print("REORGANITZANT CERCLES PER COÒPOLIS")
    print("Assignant Activity.circle segons l'Activity.organizer corresponent")
    circles = {
        5: CirclesChoices.CERCLE0,
        4: CirclesChoices.CERCLE1,
        7: CirclesChoices.CERCLE2,
        3: CirclesChoices.CERCLE3,
        2: CirclesChoices.CERCLE4,
        6: CirclesChoices.CERCLE5,
    }
    for organizer_id, circle in circles.items():
        updated = activity_model.objects.filter(organizer=organizer_id).update(
            circle=circle,
        )
        print(f"Activity actualitzats per organizer {organizer_id}: {updated}"
              f"a cercle {circle}")
        updated = stage_model.objects.filter(stage_organizer=organizer_id).update(
            circle=circle,
        )
        print(f"ProjectStage actualitzats per organizer {organizer_id}: "
              f"{updated} a cercle {circle}")
    print("Establint tots els Activity.organizer a None")
    updated = activity_model.objects.all().update(organizer=None)
    print(f"Registres actualitzats: {updated}")
    print("Eliminant tots els Organizers")
    organizer_model.objects.all().delete()


def migrate_coopsetania(
            activity_model,
            stage_model,
            organizer_model,
            entity_model,
            stagesession_model,
        ):
    """
    Coopsetània tenen entitats i organitzadores intercanviades.
    Però no tenen cercles, només l'Ateneu, incloent tenen alguns (pocs)
    registres assignats a un cercle "Coopsetània",
    que podem assumir que és el mateix ateneu però que algú l'haurà creat per
    error.

    Per tant podem assignar-ho tot al CERCLE0 i eliminar les entitats.

    Tots els d'organitzadora s'han de copiar a Entitat i assignar als registres.
    """
    print("REORGANITZANT CERCLES PER COOPSETÀNIA")
    print("assignar totes les Activity.circle al circle.CERCLE0"
          "i totes les Activity.entity a None")
    updated = activity_model.objects.all().update(
        circle=CirclesChoices.CERCLE0,
        entity=None,
    )
    print(f"{updated} registres actualitzats.")
    print("assignar totes les ProjectStageSession.entity a None.")
    updated = stagesession_model.objects.all().update(
        entity=None,
    )
    print(f"{updated} registres actualitzats.")
    print("assignar totes les ProjectStage.circle a Ateneu.")
    updated = stage_model.objects.all().update(
        circle=CirclesChoices.CERCLE0,
    )
    print(f"{updated} registres actualitzats.")
    print("eliminar tots els registres d'Entity.")
    entity_model.objects.all().delete()
    print("copiar tots els Organizer cap a Entity.")
    for organizer in organizer_model.objects.all():
        entity = entity_model(id=organizer.id, name=organizer.name)
        entity.save()
    print("per cada Activity, assignar Activity.entity = Activity.organizer.")
    for activity in activity_model.objects.all():
        if not activity.organizer:
            continue
        activity.entity_id = activity.organizer.id
        activity.save()
    print("per cada ProjectStage, assignar a tots els "
          "seus ProjectStageSession.entity = ProjectStage.stage_organizer.")
    for stage in stage_model.objects.all():
        stage.stage_sessions.all().update(
            entity=stage.stage_organizer,
        )
    print("eliminar tots els registres d'Organizer.")
    organizer_model.objects.all().delete()


def migrate_hospitalet(
            activity_model,
            stage_model,
            organizer_model,
            entity_model,
            stagesession_model,
        ):
    """
    La Col·lectiva tenen entitats i organitzadores intercanviades.
    Però no tenen cercles, només l'Ateneu.

    Per tant podem assignar-ho tot al CERCLE0 i eliminar les entitats.

    Tampoc hi ha organitzadores així que podem eliminar els valors i ja està.
    """
    print("REORGANITZANT CERCLES PER LA COL·LECTIVA")
    print("assignar totes les Activity.organizer al circle.CERCLE0,"
          "totes les Activity.entity a None"
          "i totes les Activity.organizer a None.")
    updated = activity_model.objects.all().update(
        circle=CirclesChoices.CERCLE0,
        entity=None,
        organizer=None
    )
    print(f"{updated} registres actualitzats.")
    print("assignar totes les ProjectStage.circle a Ateneu"
          "i les ProjectStage.organizer a None.")
    updated = stage_model.objects.all().update(
        circle=CirclesChoices.CERCLE0,
        stage_organizer=None,
    )
    print(f"{updated} registres actualitzats.")
    print("assignar totes les ProjectStageSession.entity a None.")
    updated = stagesession_model.objects.all().update(
        entity=None,
    )
    print(f"{updated} registres actualitzats.")
    print("eliminar tots els registres d'Entity.")
    entity_model.objects.all().delete()
    print("eliminar tots els registres d'Organizer.")
    organizer_model.objects.all().delete()


def migrate_ponentcoopera(
            activity_model,
            stage_model,
            organizer_model,
            entity_model,
            stagesession_model,
        ):
    """
    Ponentcoopera tenen entitats i organitzadores intercanviades.
    Però no tenen cercles, només l'Ateneu.

    Per tant podem assignar-ho tot al CERCLE0 i eliminar les entitats.

    Tots els d'organitzadora s'han de copiar a Entitat i assignar als registres.
    """
    print("REORGANITZANT CERCLES PER PONENTCOOPERA")
    print("assignar totes les Activity.circle al circle.CERCLE0"
          "i totes les Activity.entity a None")
    updated = activity_model.objects.all().update(
        circle=CirclesChoices.CERCLE0,
        entity=None,
    )
    print(f"{updated} registres actualitzats.")
    print("assignar totes les ProjectStageSession.entity a None.")
    updated = stagesession_model.objects.all().update(
        entity=None,
    )
    print(f"{updated} registres actualitzats.")
    print("assignar totes les ProjectStage.circle a Ateneu.")
    updated = stage_model.objects.all().update(
        circle=CirclesChoices.CERCLE0,
    )
    print(f"{updated} registres actualitzats.")
    print("eliminar tots els registres d'Entity.")
    entity_model.objects.all().delete()
    print("copiar tots els Organizer cap a Entity.")
    for organizer in organizer_model.objects.all():
        entity = entity_model(id=organizer.id, name=organizer.name)
        entity.save()
    print("per cada Activity, assignar Activity.entity = Activity.organizer.")
    for activity in activity_model.objects.all():
        if not activity.organizer:
            continue
        activity.entity_id = activity.organizer.id
        activity.save()
    print("per cada ProjectStage, assignar a tots els "
          "seus ProjectStageSession.entity = ProjectStage.stage_organizer.")
    for stage in stage_model.objects.all():
        stage.stage_sessions.all().update(
            entity=stage.stage_organizer,
        )
    print("eliminar tots els registres d'Organizer.")
    organizer_model.objects.all().delete()


def migrate_terresebre(
            activity_model,
            stage_model,
            organizer_model,
            entity_model,
            stagesession_model,
        ):
    """
    Terres de l'Ebre no tenen cercles. No obstant, a Organitzadora hi tenen un
    registre "Unió Social de Flix" que només té assignada una Activity, que
    entenc que és una entitat.

    Per tant podem assignar-ho tot al CERCLE0.

    Cal moure aquesta organitzadora Unió Social de Flix cap a Entity.
    Cal assignar l'Activity.entity que té Unió Social de Flix.
    """
    print("REORGANITZANT CERCLES PER TERRES DE L'EBRE")
    print("assignar totes les Activity.circle al circle.CERCLE0"
          "i totes les Activity.entity a None")
    updated = activity_model.objects.all().update(
        circle=CirclesChoices.CERCLE0,
    )
    print(f"{updated} registres actualitzats.")
    print("assignar totes les ProjectStage.circle a Ateneu.")
    updated = stage_model.objects.all().update(
        circle=CirclesChoices.CERCLE0,
    )
    print(f"{updated} registres actualitzats.")
    print("crear la Entity que ara hi ha a Organizer.")
    new_entity = entity_model(name="Unió Social de Flix")
    new_entity.save()
    print("posar la (les?) Activity.entity a la que té com a organizer Unió Social "
          "de Flix.")
    updated = activity_model.objects.filter(organizer=5).update(
        entity=new_entity,
    )
    print(f"{updated} registres actualitzats.")
    print("eliminar tots els registres d'Organizer.")
    organizer_model.objects.all().delete()


def migrate_terresgironines(
            activity_model,
            stage_model,
            organizer_model,
            entity_model,
            stagesession_model,
        ):
    """
    Terres Gironines ho tenen perfectament bé, només cal traslladar els
    Organizers com a .circle i fer neteja.

    """
    print("REORGANITZANT CERCLES PER TERRES GIRONINES")
    print("Assignant Activity.circle segons l'Activity.organizer corresponent")
    circles = {
        12: CirclesChoices.CERCLE0,
        13: CirclesChoices.CERCLE1,
        14: CirclesChoices.CERCLE2,
        15: CirclesChoices.CERCLE3,
    }
    for organizer_id, circle in circles.items():
        updated = activity_model.objects.filter(organizer=organizer_id).update(
            circle=circle,
        )
        print(f"Activity actualitzats per organizer {organizer_id}: {updated}"
              f"a cercle {circle}")
        updated = stage_model.objects.filter(stage_organizer=organizer_id).update(
            circle=circle,
        )
        print(f"ProjectStage actualitzats per organizer {organizer_id}: "
              f"{updated} a cercle {circle}")
    print("Establint tots els Activity.organizer a None")
    updated = activity_model.objects.all().update(organizer=None)
    print(f"Registres actualitzats: {updated}")
    print("Eliminant tots els Organizers")
    organizer_model.objects.all().delete()


def migrate_vallesoccidental(
            activity_model,
            stage_model,
            organizer_model,
            entity_model,
            stagesession_model,
        ):
    """
    Camp entitat: està tot correcte i no cal tocar res.
    Camp organitzadora: el feien servir com a una dada interna que s'havien
    inventat, es pot eliminar sense haver-lo de migrar enlloc.
    Ateneu/Cercle: tot a Ateneu (no teníen cap cercle. A partir de 2022 en
    tindran 2).
    """
    print("REORGANITZANT CERCLES PER VALLÈS OCCIDENTAL")
    print("assignar totes les Activity.circle al circle.CERCLE0"
          "i totes les Activity.entity a None")
    updated = activity_model.objects.all().update(
        circle=CirclesChoices.CERCLE0,
    )
    print(f"{updated} registres actualitzats.")
    print("assignar totes les ProjectStage.circle a Ateneu.")
    updated = stage_model.objects.all().update(
        circle=CirclesChoices.CERCLE0,
    )
    print(f"{updated} registres actualitzats.")
    print("Eliminant tots els Organizers")
    organizer_model.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('coopolis', '0094_projectstage_circle'),
        ('cc_courses', '0055_activity_circle'),
    ]

    operations = [
        migrations.RunPython(migrate_organizer_to_circle),
    ]
