# Generated by Django 2.2.7 on 2020-05-13 12:06

from django.db import migrations


def populate_mail_templates(apps, schema_editor):
    mail_model = apps.get_model('mailing_manager', 'Mail')
    mail_model.objects.bulk_create([
        mail_model(
            text_identifier='EMAIL_NEW_PROJECT',
            subject="Nova sol·licitud d'acompanyament: {projecte_nom}",
            body="""<h2>Nova sol·licitud d'acompanyament</h2><br /><br />
Nom del projecte: {projecte_nom} <br />
Telèfon de contacte: {projecte_telefon} <br />
Correu electrònic de contacte del projecte: {projecte_email} <br />
Correu electrònic de l'usuari que l'ha creat: {usuari_email} <br />""",
            default_template_path='emails/front_generic.html'
        ),
        mail_model(
            text_identifier='EMAIL_ENROLLMENT_CONFIRMATION',
            subject="Confirmació d'inscripció a l'activitat: {activitat_nom}",
            body="""
<table align="center" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#f0f0f0">
<tr>
  <td align="center" valign="top" class="em_text1 pad10">
    <p>T'has inscrit a la formació</p>
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
    <p style="margin-left: 60px"><strong>Data:</strong> {activitat_data_inici}</p>
    <p style="margin-left: 60px"><strong>Hora:</strong> {activitat_hora_inici}</p>
    <p style="margin-left: 60px"><strong>Lloc:</strong> {activitat_lloc}</p>
    <p style="padding-top: 20px">Es tracta d'una formació gratuïta subvencionada, per això et demanem que, si
      finalment no pots venir, ens avisis amb antelació per poder obrir la plaça a una altra persona.<br>
      Per fer-ho pots gestionar les teves inscripcions accedint a l'aplicació amb el teu compte i anant a 
    l'apartat <a href="{absolute_url_my_activities}">Perfil -> Els Meus Cursos</a>.</p>
  </td>
</tr>
<tr>
  <td align="center" class="em_text1 pad10" bgcolor="#fafafa" style="padding-bottom: 15px;">
    <a href="{url_web_ateneu}" style="color:#e94e1b; text-decoration:none; font-weight: bold;">Fins aviat!</a>
  </td>
</tr>
</table>
""",
            default_template_path='emails/front_generic.html'
        ),
        mail_model(
            text_identifier='EMAIL_ENROLLMENT_WAITING_LIST',
            subject="Ets en llista d'espera per l'activitat: {activitat_nom}",
            body="""
<table align="center" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#f0f0f0">
<tr>
  <td align="center" valign="top" class="em_text1 pad10">
    <p>Has entrat en llista d'espera per participar a la formació</p>
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
    <p style="margin-left: 60px"><strong>Data:</strong> {activitat_data_inici}</p>
    <p style="margin-left: 60px"><strong>Hora:</strong> {activitat_hora_inici}</p>
    <p style="margin-left: 60px"><strong>Lloc:</strong> {activitat_lloc}</p>
    <p style="padding-top: 20px">Si queda una plaça disponible, automàticament s'assignarà a la següent persona de la 
    llista d'espera. De donar-se el cas, rebràs un correu electrònic informant-te que la teva inscripció ha estat 
    confirmada. Sempre pots comprovar l'estat de la teva inscripció accedint a l'aplicació amb el teu compte i anant a 
    l'apartat <a href="{url_els_meus_cursos}">Perfil -> Els Meus Cursos</a>.</p>
  </td>
</tr>
<tr>
  <td align="center" class="em_text1 pad10" bgcolor="#fafafa" style="padding-bottom: 15px;">
    <a href="{url_ateneu}" style="color:#e94e1b; text-decoration:none; font-weight: bold;">Fins aviat!</a>
  </td>
</tr>
</table>""",
            default_template_path='emails/front_generic.html'
        ),
        mail_model(
            text_identifier='EMAIL_ENROLLMENT_REMINDER',
            subject="Recordatori d'inscripció a l'activitat: {activitat_nom}",
            body="""
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
    <strong>{activitat_nom}</strong> de {ateneu_nom}
  </td>
</tr>
<tr>
  <td height="25" class="em_h20" style="font-size:0px; line-height:0px; height:25px;">&nbsp;</td>
</tr>
<tr>
  <td align="left" valign="top" style="padding: 0px 40px 10px 40px" bgcolor="#fafafa" class="em_text1 pad10">
    <p style="margin-left: 60px"><strong>Data:</strong> {activitat_data_inici}</p>
    <p style="margin-left: 60px"><strong>Hora:</strong> {activitat_hora_inici}</p>
    <p style="margin-left: 60px"><strong>Lloc:</strong> {activitat_lloc}</p>
    <p style="padding-top: 20px">Es tracta d'una formació gratuïta subvencionada, per això et demanem que, si
      finalment no pots venir, ens avisis amb antelació per poder obrir la plaça a una altra persona.<br>
      Per fer-ho pots gestionar les teves inscripcions accedint a l'aplicació amb el teu compte i anant a 
    l'apartat <a href="{absolute_url_my_activities}">Perfil -> Els Meus Cursos</a>.</p>
  </td>
</tr>
<tr>
  <td align="center" class="em_text1 pad10" bgcolor="#fafafa" style="padding-bottom: 15px;">
    <a href="{url_web_ateneu}" style="color:#e94e1b; text-decoration:none; font-weight: bold;">Fins aviat!</a>
  </td>
</tr>
</table>""",
            default_template_path='emails/front_generic.html'
        ),
        mail_model(
            text_identifier='EMAIL_SIGNUP_WELCOME',
            subject="Nou compte creat a {ateneu_nom}",
            body="""
<h2>Benvingut/da a {ateneu_nom}!</h2>
<p><em>Estàs rebent aquest correu perquè s'ha completat un registre a la plataforma {url_backoffice}.<br />
Si aquest registre no l'has fet tu o cap altra persona amb qui comparteixis aquest compte, ignora aquest correu o 
avisa'ns per tal que l'eliminem de la base de dades.</em></p><br />
<p>Amb el teu compte pots:</p>
<ul>
<li>Inscriure't a les sessions formatives, que trobaràs <a href="{url_accions}">aquí</a>.</li>
<li>Si esteu iniciant o teniu en marxa un projecte cooperatiu, podeu 
<a href="{url_projecte}">sol·licitar un acompanyament</a>.</li>
<li>Consultar o editar les dades del teu perfil i recuperar la contrassenya. </li>
</ul>
<p>Més informació a <a href="{url_backoffice}">{url_backoffice}</a>.</p>""",
            default_template_path='emails/front_single_text.html'
        ),
        mail_model(
            text_identifier='EMAIL_ADDED_TO_PROJECT',
            subject="Has estat afegit com a participant del projecte {projecte_nom}",
            body="""
<p>Has estat afegit com a participant al projecte acompanyat per {ateneu_nom}:</p>
<h3>{projecte_nom}</h3>
<p>Per veure i modificar la fitxa del vostre projecte, accedeix a <a href="{url_projectes}">l'apartat Projectes</a> de la 
plataforma de {ateneu_nom} amb el teu e-mail i contrasenya.</p><br />
<p>Si necessites la contrasenya, trobaràs l'opció per fer-ho a <a href="{url_backoffice}">{url_backoffice}</a>.</p>""",
            default_template_path='emails/front_single_text.html'
        ),
        mail_model(
            text_identifier='EMAIL_PASSWORD_RESET',
            subject="Reinici de contrasenya a {ateneu_nom}",
            body="""
<p>Has rebut aquest correu perquè hi ha hagut una sol·licitud de reinici de contrasenya del teu compte a {url_backoffice}.</p><br />
<p>Si has fet tu la sol·licitud, si us plau obre el següent enllaç i escull una contrasenya nova: (password_reset_url)</p>
<p>Si no has fet tu la sol·licitud, senzillament ignora aquest correu.</p><br />
<p>El teu nom d'usuari, en cas que l'hagis oblidat: {user_email}</p><br />
<p>Gràcies per fer servir la nostra plataforma.</p>""",
            default_template_path='emails/front_single_text.html'
        )
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('coopolis', '0051_user_project_involved'),
        # ('mailing_manager', '0001_initial'),
    ]

    operations = [
        # migrations.RunPython(populate_mail_templates),
    ]
