from django.db import models


class County(models.Model):
    name = models.CharField("nom", max_length=50)

    class Meta:
        verbose_name = "comarca"
        verbose_name_plural = "comarques"
        ordering = ["name", ]

    def __str__(self):
        return self.name


class Town(models.Model):
    class Meta:
        verbose_name = "població"
        verbose_name_plural = "poblacions"
        ordering = ["name", ]

    county = models.ForeignKey(
        County,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
    )
    name = models.CharField("nom", max_length=250)
    name_for_justification = models.CharField(
        "nom",
        max_length=250,
        default="",
        blank=True,
    )

    def __str__(self):
        return self.name
