from django.db import models


class ServicesChoices(models.IntegerChoices):
    __empty__ = "Cap"
    MAP_DIAGNOSI = 1, "Servei de mapatge i diagnosi"
    DIV_SENS_GEN_CONEIXEMENT = 2, ("Servei de Divulgació, Sensibilització i "
    "Generació de Coneixement.")
    FORM_PROM_CREA_CONS = 3, ("Servei de Formació per a la promoció, creació "
    "i consolidació de cooperatives i projectes de l'ESS.")
    ACOM_CREA_CONS = 4, ("Servei d'Acompanyament per la creació i "
    "consolidació de cooperatives i projectes de l'ESS.")
    INTERCOOP_XARXA_TERRITORI = 5, ("Servei de Facilitació de la "
    "Intercooperació, treball en xarxa i dinamització territorial.")
    PUNT_INFO = 6, "Punt d'informació sobre l'ESS."
