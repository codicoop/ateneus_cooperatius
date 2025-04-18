# Generated by Django 2.2.7 on 2021-09-08 14:54

from django.db import migrations


def populate_mail_templates(apps, schema_editor):
    # Migration disabled because it references the deprecated package
    # mailing_manager.

    print('')
    mail_model = apps.get_model('mailing_manager', 'Mail')

    obj, created = mail_model.objects.update_or_create(
        text_identifier='EMAIL_ENROLLMENT_POLL',
        defaults={
            'text_identifier': 'EMAIL_ENROLLMENT_POLL',
            'subject': "Enquesta de valoració de {activitat_nom}",
            'body': """<table align="center" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#f0f0f0">
    <tr>
      <td align="center" valign="top" class="em_text1 pad10">
        <p>Enquesta de valoració</p>
      </td>
    </tr>
    <tr>
      <td height="15" style="font-size:0px; line-height:0px; height:15px;">&nbsp;</td>
    </tr>
    <tr>
      <td align="center" valign="top" style="font-family:'Open Sans', Arial, sans-serif; font-size:22px;
      line-height:22px; color:#000; letter-spacing:2px; padding-bottom:12px;" class="pad10">
        <strong>{activitat_nom}</strong> de {ateneu_nom}
      </td>
    </tr>
    <tr>
      <td height="25" class="em_h20" style="font-size:0px; line-height:0px; height:25px;">&nbsp;</td>
    </tr>
    <tr>
      <td align="left" valign="top" style="padding: 0px 40px 10px 40px" bgcolor="#fafafa" class="em_text1 pad10">
        <p style="padding-top: 20px">Hola {persona_nom}!</p>
        <p style="padding-top: 20px">T'enviem aquest correu perquè has participat a aquesta sessió:</p>
        <p style="margin-left: 60px"><strong>Data:</strong> {activitat_data_inici}</p>
        <p style="margin-left: 60px"><strong>Hora:</strong> {activitat_hora_inici}</p>
        <p style="margin-left: 60px"><strong>Lloc:</strong> {activitat_lloc}</p>
        <p style="padding-top: 20px">{poll_reminder_body}</p>
        <p style="padding-top: 20px">Els resultats de les enquestes de valoració 
        son una eina imprescindible pel funcionament d'aquesta formació 
        gratuïta subvencionada.</p>
        <p style="padding-top: 20px">Si us plau, omple <a href="{absolute_url_poll}">l'enquesta de valoració</a>.
        </p> 
        <p style="padding-top: 20px">{absolute_url_activity}</p>
        <p>
          Pots gestionar les teves dades i inscripcions accedint a l'aplicació amb el teu compte i anant a 
        l'apartat <a href="{absolute_url_my_activities}">Perfil -> Els Meus Cursos</a>.</p>
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
    print('EMAIL_ENROLLMENT_POLL template updated.')


class Migration(migrations.Migration):

    dependencies = [
        ('coopolis', '0103_projectstagesession_justification_file'),
    ]

    operations = [
        # Migration disabled because it references the deprecated package
        # mailing_manager.
        # migrations.RunPython(populate_mail_templates),
    ]
