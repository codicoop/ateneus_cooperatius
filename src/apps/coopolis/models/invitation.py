from django.db import models
import uuid


class Invitation(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey(
        "User",
        verbose_name="usuari",
        on_delete=models.CASCADE,
        related_name="invitations",
    )
    project = models.ForeignKey(
        "coopolis.project",
        verbose_name="projecte",
        on_delete=models.CASCADE,
        related_name="invitations",
    )
    is_invited = models.BooleanField(default=False)
    created = models.DateTimeField(verbose_name="creació", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="actualització", auto_now=True)

    class Meta:
        verbose_name = "invitació"
        verbose_name_plural = "invitacions"
        ordering = ["created", ]
