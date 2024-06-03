from django.db import models

from apps.coopolis.storage_backends import PublicMediaStorage


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

    def __str__(self):
        return self.name


class Customization(models.Model):
    logo = models.ImageField(
        "Logotip",
        help_text="Mides aprox: 400px d'amplada x 200px d'alçada. Idealment, fons transparent.",
        storage=PublicMediaStorage(),
        null=True,
        blank=False,
    )
    signatures_pdf_footer = models.ImageField(
        "Imatge del peu de pàgina de signatures",
        help_text="Mides: 1.241px d'amplada x 280px d'alçada. Fons blanc.",
        storage=PublicMediaStorage(),
        null=True,
        blank=False,
    )

    class Meta:
        verbose_name = "Configuració de l'aplicació"
        verbose_name_plural = "Configuració de l'aplicació"

    def __str__(self):
        return "Valors de configuració de l'aplicació"
