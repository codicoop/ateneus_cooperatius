# Generated by Django 2.2.7 on 2020-08-07 07:45

from django.db import migrations


def populate_mail_templates(apps, schema_editor):
    # Migration disabled because it references the deprecated package
    # mailing_manager.

    print('')
    mail_model = apps.get_model('mailing_manager', 'Mail')

    obj, created = mail_model.objects.update_or_create(
        text_identifier='EMAIL_PASSWORD_RESET',
        defaults={
            'text_identifier': 'EMAIL_PASSWORD_RESET',
            'subject': "Reinicialització de contrasenya del teu compte a {ateneu_nom}",
            'body': """<table align="center" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#f0f0f0">
    <tr>
      <td align="center" valign="top" class="em_text1 pad10">
        <p>Instruccions per reiniciar la contrasenya</p>
      </td>
    </tr>
    <tr>
      <td height="15" style="font-size:0px; line-height:0px; height:15px;">&nbsp;</td>
    </tr>
    <tr>
      <td align="left" valign="top" style="padding: 0px 40px 10px 40px" bgcolor="#fafafa" class="em_text1 pad10">
        <p style="padding-top: 20px">Hola {persona_nom}!</p>
        <p style="padding-top: 20px">T'enviem aquest correu perquè algú ha 
            sol·licitat el reinici de la contrasenya del compte {persona_email}
            a {absolute_url}</p>
        <p style="margin-left: 60px">Si no has estat tu qui ho ha demanat, 
            ignora aquest correu. Si segueixes rebent aquest correu repetidament,
            podria voler dir que algú està intentant obtenir accés al teu 
            compte, et recomanem que posis una contrasenya el més llarga 
            possible i que avisis a les administradores de l'Ateneu.</p>
        <p style="margin-left: 60px">Per establir una nova contrasenya fes
            servir aquest enllaç: {password_reset_url}</p>
      </td>
    </tr>
    <tr>
      <td align="center" class="em_text1 pad10" bgcolor="#fafafa" style="padding-bottom: 15px;">
        <a href="{url_web_ateneu}" style="color:#e94e1b; text-decoration:none; font-weight: bold;">Fins aviat!</a>
      </td>
    </tr>
    </table>""",
            'default_template_path': 'emails/front_generic.html'
        },
    )
    print('EMAIL_PASSWORD_RESET template updated.')


class Migration(migrations.Migration):

    dependencies = [
        ('coopolis', '0088_auto_20211108_0936'),
    ]

    operations = [
        # Migration disabled because it references the deprecated package
        # mailing_manager.
        # migrations.RunPython(populate_mail_templates),
    ]
