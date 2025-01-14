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
  <td height="25" class="em_h20" style="font-size:0px; line-height:0px; height:25px;">&nbsp;</td>
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
