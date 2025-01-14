import logging

from django.db import migrations

from conf.post_office import textify, get_default_email_template


def populate_mail_templates(apps, schema_editor):
    mail_model = apps.get_model("post_office", "EmailTemplate")

    templates = [
        dict(
            id="EMAIL_NEW_PROJECT",
            translated_templates={
                "ca": {
                    "subject": "Nova sol·licitud d'acompanyament: {{projecte_nom}}",
                    "body": get_default_email_template(
                        """
<table align="center" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#f0f0f0">
<tr>
  <td align="center" valign="top" class="em_text1 pad10">
    <p>Nova sol·licitud d'acompanyament</p>
  </td>
</tr>
<tr>
  <td height="15" style="font-size:0px; line-height:0px; height:15px;">&nbsp;</td>
</tr>
<tr>
  <td align="left" valign="top" style="padding: 0px 40px 10px 40px" bgcolor="#fafafa" class="em_text1 pad10">
    <p style="margin-left: 60px"><strong>Nom del projecte:</strong> {{projecte_nom}}</p>
    <p style="margin-left: 60px"><strong>Telèfon de contacte:</strong> {{projecte_telefon}}</p>
    <p style="margin-left: 60px"><strong>Correu electrònic de contacte del projecte:</strong> {{projecte_email}}</p>
    <p style="margin-left: 60px"><strong>Correu electrònic de l'usuari que l'ha creat:</strong> {{usuari_email}}</p>
  </td>
</tr>
</table>
"""
                    ),
                },
            },
        ),
        dict(
            id="EMAIL_PROJECT_REQUEST_CONFIRMATION",
            translated_templates={
                "ca": {
                    "subject": "Nova sol·licitud d'acompanyament: {{projecte_nom}}",
                    "body": get_default_email_template(
                        """
<table align="center" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#f0f0f0">
<tr>
  <td align="center" valign="top" class="em_text1 pad10">
    <p>Confirmació de sol·licitud d'acompanyament pel projecte {{projecte_nom}}</p>
  </td>
</tr>
<tr>
  <td height="15" style="font-size:0px; line-height:0px; height:15px;">&nbsp;</td>
</tr>
<tr>
  <td align="left" valign="top" style="padding: 0px 40px 10px 40px" bgcolor="#fafafa" class="em_text1 pad10">
  <p style="padding-top: 20px">En els propers dies una persona de l'equip de 
    l'ateneu cooperatiu es posarà en contacte amb tu per parlar dels propers 
    passos.</p>
    <p style="padding-top: 20px">Per consultar i modificar la fitxa del projecte 
    accedeix a <a href="{{url_backoffice}}">l'aplicació dels serveis de l'ateneu</a>.</p>
  </td>
</tr>
</table>
"""
                    ),
                },
            },
        ),
        dict(
            id="EMAIL_ENROLLMENT_REMINDER",
            translated_templates={
                "ca": {
                    "subject": "Recordatori d'inscripció a l'activitat: {{activitat_nom}}",
                    "body": get_default_email_template(
                        """
<table align="center" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#f0f0f0">
<tr>
  <td align="center" valign="top" class="em_text1 pad10">
    <p>Recordatori d'inscripció</p>
  </td>
</tr>
<tr>
  <td height="15" style="font-size:0px; line-height:0px; height:15px;">&nbsp;</td>
</tr>
<tr>
  <td align="center" valign="top" style="font-family:'Open Sans', Arial, sans-serif; font-size:22px;
  line-height:22px; color:#000; letter-spacing:2px; padding-bottom:12px;" class="pad10">
    <strong>{{activitat_nom}}</strong> de {{ateneu_nom}}
  </td>
</tr>
<tr>
  <td height="25" class="em_h20" style="font-size:0px; line-height:0px; height:25px;">&nbsp;</td>
</tr>
<tr>
  <td align="left" valign="top" style="padding: 0px 40px 10px 40px" bgcolor="#fafafa" class="em_text1 pad10">
    <p style="margin-left: 60px"><strong>Data:</strong> {{activitat_data_inici}}</p>
    <p style="margin-left: 60px"><strong>Hora:</strong> {{activitat_hora_inici}}</p>
    <p style="margin-left: 60px"><strong>Lloc:</strong> {{activitat_lloc}}</p>
    <p style="padding-top: 20px">Es tracta d'una formació gratuïta subvencionada, per això et demanem que, si
      finalment no pots venir, ens avisis amb antelació per poder obrir la plaça a una altra persona.<br>
      Per fer-ho pots gestionar les teves inscripcions accedint a l'aplicació amb el teu compte i anant a 
    l'apartat <a href="{{absolute_url_my_activities}}">Perfil -> Els Meus Cursos</a>.</p>
  </td>
</tr>
<tr>
  <td align="center" class="em_text1 pad10" bgcolor="#fafafa" style="padding-bottom: 15px;">
    <a href="{{url_web_ateneu}}" style="color:#e94e1b; text-decoration:none; font-weight: bold;">Fins aviat!</a>
  </td>
</tr>
</table>
"""
                    ),
                },
            },
        ),
        dict(
            id="EMAIL_SIGNUP_WELCOME",
            translated_templates={
                "ca": {
                    "subject": "Nou compte creat a {{ateneu_nom}}",
                    "body": get_default_email_template(
                        """
<table align="center" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#f0f0f0">
<tr>
  <td align="center" valign="top" class="em_text1 pad10">
    <p>Benvingut/da a {{ateneu_nom}}!</p>
  </td>
</tr>
<tr>
  <td height="15" style="font-size:0px; line-height:0px; height:15px;">&nbsp;</td>
</tr>
<tr>
  <td align="left" valign="top" style="padding: 0px 40px 10px 40px" bgcolor="#fafafa" class="em_text1 pad10">
  <p style="padding-top: 20px"><em>Estàs rebent aquest correu perquè s'ha completat un registre a la plataforma <a href=\"{{url_backoffice}}\">{{url_backoffice}}</a>.<br />
    Si aquest registre no l'has fet tu o cap altra persona amb qui comparteixis aquest compte, ignora aquest correu o 
    avisa'ns per tal que l'eliminem de la base de dades.</em></p>
  <p style="padding-top: 20px">Amb el teu compte pots:</p>
  <ul>
    <li>Inscriure't a les sessions formatives, que trobaràs <a href="{{url_accions}}">aquí</a>.</li>
    <li>Si esteu iniciant o teniu en marxa un projecte cooperatiu, podeu <a href="{{url_projecte}}">sol·licitar un acompanyament</a>.</li>
    <li>Consultar o editar les dades del teu perfil i recuperar la contrassenya. </li>
  </ul>

  <p style="padding-top: 20px">Més informació a <a href="{{url_backoffice}}">{{url_backoffice}}</a>.</p>
  </td>
</tr>
</table>
""",
                    ),
                },
            },
        ),
        dict(
            id="EMAIL_PASSWORD_RESET",
            translated_templates={
                "ca": {
                    "subject": "Reinicialització de contrasenya del teu compte a {{ateneu_nom}}",
                    "body": get_default_email_template(
                        """
<table align="center" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#f0f0f0">
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
        <p style="padding-top: 20px">Hola {{persona_nom}}!</p>
        <p style="padding-top: 20px">T'enviem aquest correu perquè algú ha 
            sol·licitat el reinici de la contrasenya del compte {{persona_email}}
            a {{absolute_url}}</p>
        <p style="margin-left: 60px">Si no has estat tu qui ho ha demanat, 
            ignora aquest correu. Si segueixes rebent aquest correu repetidament,
            podria voler dir que algú està intentant obtenir accés al teu 
            compte, et recomanem que posis una contrasenya el més llarga 
            possible i que avisis a les administradores de l'Ateneu.</p>
        <p style="margin-left: 60px">Per establir una nova contrasenya fes
            servir aquest enllaç: <a href=\"{{password_reset_url}}\">{{password_reset_url}}</a></p>
      </td>
    </tr>
    <tr>
      <td align="center" class="em_text1 pad10" bgcolor="#fafafa" style="padding-bottom: 15px;">
        <a href="{{url_web_ateneu}}" style="color:#e94e1b; text-decoration:none; font-weight: bold;">Fins aviat!</a>
      </td>
    </tr>
    </table>
""",
                    ),
                },
            },
        ),
    ]

    for template in templates:
        obj, created = mail_model.objects.update_or_create(
            name=template.get("id"),
            language="",
            defaults={
                "name": template.get("id"),
            },
        )
        for lang, translated_template in template.get("translated_templates").items():
            obj.translated_templates.update_or_create(
                # name field included due this bug:
                # https://github.com/ui/django-post_office/issues/214
                name=template.get("id"),
                language=lang,
                defaults={
                    "subject": translated_template.get("subject"),
                    "html_content": translated_template.get("body"),
                    "content": textify(translated_template.get("body")),
                },
            )
            logging.info(
                f"E-mail template '{template.get('id')}' updated or created."
            )


class Migration(migrations.Migration):

    dependencies = [
        ("coopolis", "0132_data_email_project_invitation"),
        ("post_office", "__latest__"),
    ]

    operations = [
        migrations.RunPython(populate_mail_templates),
    ]
