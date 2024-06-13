from django.db import migrations


def populate_mail_templates(apps, schema_editor):
    print('')
    mail_model = apps.get_model('mailing_manager', 'Mail')

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
        ('coopolis', '0131_data_email_project_invitation'),
    ]

    operations = [
        migrations.RunPython(populate_mail_templates),
    ]
