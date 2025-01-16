from django.db import migrations


def populate_mail_templates(apps, schema_editor):
    # Migration disabled because it references the deprecated package
    # mailing_manager.

    print('')
    mail_model = apps.get_model('mailing_manager', 'Mail')

    obj, created = mail_model.objects.update_or_create(
        text_identifier='EMAIL_PROJECT_INVITATION',
        defaults={
            'text_identifier': 'EMAIL_PROJECT_INVITATION',
            'subject': "Invitació per a formar part del projecte {project}",
            'body': """
                <p>Hola {persona_fullname}!</p>
                <p>T'enviem aquest correu perquè t'han afegit com a soci del
                 projecte {project}, acompanyat per l'ateneu cooperatiu.</p>
                
                <p>Per a confirmar la teva adhesió visita el següent enllaç: 
                <a href="{invitation_url}">{invitation_url}</a>
                </p>
                
                <p>Gràcies i una salutació</p>
    """,
            'default_template_path': 'emails/front_generic.html'
        },
    )
    print('EMAIL_PROJECT_INVITATION template updated.')

    obj, created = mail_model.objects.update_or_create(
        text_identifier='EMAIL_PARTNER_ELIMINATION',
        defaults={
            'text_identifier': 'EMAIL_PARTNER_ELIMINATION',
            'subject': "Eliminació de soci/a en el projecte {project}",
            'body': """
                <p>Hola!</p>
                <p>T'enviem aquest correu per a comunicar-te que en el dia d'avui 
                s'ha eliminat del projecte {project} al soci o sòcia 
                {persona_fullname} amb correu electrònic {persona_email}</p>

                <p>Salutacions</p>
    """,
            'default_template_path': 'emails/front_generic.html'
        },
    )
    print('EMAIL_PARTNER_ELIMINATION template updated.')


class Migration(migrations.Migration):
    dependencies = [
        ('coopolis', '0131_auto_20240625_1600'),
    ]

    operations = [
        # Migration disabled because it references the deprecated package
        # mailing_manager.
        # migrations.RunPython(populate_mail_templates),
    ]
