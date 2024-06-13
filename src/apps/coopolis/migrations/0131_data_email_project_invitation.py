from django.db import migrations


def populate_mail_templates(apps, schema_editor):
    print('')
    mail_model = apps.get_model('mailing_manager', 'Mail')

    obj, created = mail_model.objects.update_or_create(
        text_identifier='EMAIL_PROJECT_INVITATION',
        defaults={
            'text_identifier': 'EMAIL_PROJECT_INVITATION',
            'subject': "Invitació per a formar part del projecte {project}",
            'body': """
                <p>Hola {persona_fullname}!</p>
                <p>T'enviem aquest correu perquè avui
                has estat convidat a formar part del projecte {project}.</p>
                
                <p>Per a confirmar la teva adhesió deus visitant el següent enllaç 
                i acceptar la invitació:
                <a href="{invitation_url}">{invitation_url}</a>
                </p>
                
                <p>Gràcies i una salutació</p>
    """,
            'default_template_path': 'emails/front_generic.html'
        },
    )
    print('EMAIL_PROJECT_INVITATION template updated.')


class Migration(migrations.Migration):
    dependencies = [
        ('coopolis', '0130_auto_20240613_0903'),
    ]

    operations = [
        migrations.RunPython(populate_mail_templates),
    ]
