from django.db import models


class ProjectStageStatesChoices(models.TextChoices):
    OPEN = "OPEN", "Obert"
    CLOSE = "CLOSE", "Tancat"
    PENDING = "PENDING", "Pendent"


class StageTypeChoices(models.TextChoices):
    CREATION = "11", "Creació"
    CONSOLIDATION = "12", "Consolidació"
    INCUBATION = "9", "Incubació"