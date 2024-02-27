from django.db import models


class ProjectStageStatesChoices(models.TextChoices):
    PENDING = "PENDING", "En procés"
    OPEN = "OPEN", "Sol·licitat"
    CLOSE = "CLOSE", "Finalizat"


class StageTypeChoices(models.TextChoices):
    CREATION = "11", "Creació"
    CONSOLIDATION = "12", "Consolidació"
    INCUBATION = "9", "Incubació"