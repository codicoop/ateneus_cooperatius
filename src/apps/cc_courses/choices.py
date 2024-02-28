from django.db import models


class ProjectStageStatesChoices(models.TextChoices):
    PENDING = "PENDING", "Sol·licitat"
    OPEN = "OPEN", "En procés"
    CLOSE = "CLOSE", "Finalizat"


class StageTypeChoices(models.TextChoices):
    CREATION = "11", "Creació"
    CONSOLIDATION = "12", "Consolidació"
    INCUBATION = "9", "Incubació"