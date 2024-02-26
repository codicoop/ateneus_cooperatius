from django.db import models


class ProjectStageStatesChoices(models.TextChoices):
    OPEN = "OPEN", "Obert"
    CLOSE = "CLOSE", "Tancat"
    PENDING = "PENDING", "Pendent"
