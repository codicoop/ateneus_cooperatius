from django.db import models


class ProjectStageStatesChoices(models.TextChoices):
    __empty__ = "Sense indicar"
    PENDING = "PENDING", "Sol·licitat"
    OPEN = "OPEN", "En procés"
    CLOSE = "CLOSE", "Finalitzat"


class StageTypeChoices(models.TextChoices):
    CREATION = "11", "Creació"
    CONSOLIDATION = "12", "Consolidació"
    INCUBATION = "9", "Incubació"