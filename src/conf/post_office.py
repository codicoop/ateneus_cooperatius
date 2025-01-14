import re

from constance import config
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import get_language
from post_office import mail as base_mail

from apps.coopolis.models.general import Customization


def send(
    recipients=None,
    sender=None,
    template=None,
    context=None,
    subject="",
    message="",
    html_message="",
    scheduled_time=None,
    expires_at=None,
    headers=None,
    priority=None,
    attachments=None,
    render_on_delivery=False,
    log_level=None,
    commit=True,
    cc=None,
    bcc=None,
    language="",
    backend="",
):
    if not language:
        language = get_language()
    return base_mail.send(
        recipients=recipients,
        sender=sender,
        template=template,
        context=context,
        subject=subject,
        message=message,
        html_message=html_message,
        scheduled_time=scheduled_time,
        expires_at=expires_at,
        headers=headers,
        priority=priority,
        attachments=attachments,
        render_on_delivery=render_on_delivery,
        log_level=log_level,
        commit=commit,
        cc=cc,
        bcc=bcc,
        language=language,
        backend=backend,
    )


def textify(html):
    # Remove html tags and continuous whitespaces
    text_only = re.sub("[ \t]+", " ", strip_tags(html))
    # Strip single spaces in the beginning of each line
    return text_only.replace("\n ", "\n").strip()


def get_default_email_template(mail_content):
    """
    We were originally using the mailing_manager package, which is a wrapper
    of the mail_queue package, and the way it worked was that every email
    template in the database had a .html template assigned, so every time it
    sent an email it was rendered using this .html.
    Now we switched to django-post-office, and this package does not include a
    way to render from an .html template. Instead, the whole template is
    stored in the database.

    This function was created to be used in the data migrations that create the
    email templates in the database, so the entire html template is rendered and
    included there.
    """
    html = render_to_string(
        "emails/front_generic.html",
        context={
            "mail_content": mail_content,
            "config": config,
            "customization": Customization.objects.first(),
        },
    )
    return html
