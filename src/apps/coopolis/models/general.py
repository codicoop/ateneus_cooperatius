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

    name = models.CharField("nom", max_length=250)

    def __str__(self):
        return self.name
