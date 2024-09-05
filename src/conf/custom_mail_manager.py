from constance import config

from mailing_manager.mail_queue_handler import MailQueueHandler


class MyMailTemplate(MailQueueHandler):
    debug_bcc = config.EMAIL_TO_DEBUG
    template = 'emails/front_generic.html'

    def send_to_user(self, user_obj, now=False):
        if not user_obj.fake_email:
            self.to = user_obj.email
            super().send(now=now)

    @property
    def template_extra_context(self):
        from apps.coopolis.context_processors import get_customization_context
        return {
            "config": config,
            **get_customization_context(),
        }
