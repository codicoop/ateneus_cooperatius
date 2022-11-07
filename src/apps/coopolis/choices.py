import sys

from django.conf import settings
from django.db import models


class ServicesChoices(models.IntegerChoices):
    __empty__ = "Cap"
    MAP_DIAGNOSI = 10, "1) Mapeig i diagnosi"
    DIV_SENS_GEN_CONEIXEMENT = 20, (
        "2) Divulgació, sensibilització i generació coneixement"
    )
    FORM_PROM_CREA_CONS = 30, (
        "3) Formació per a la promoció, creació i consolidació "
    )
    ACOM_CREA_CONS = 40, (
        "4) Acompanyament per a la creació i consolidació "
    )
    INTERCOOP_XARXA_TERRITORI = 50, (
        "5) Facilitació intercooperació, treball en xarxa i dinamització "
        "territori"
    )
    PUNT_INFO = 60, "6) Punt d'informació sobre ESS"
    SERV_COMPLEMENTARIS = 70, "7) Serveis Complementaris"

    def get_sub_services(self):
        range_start = self.value * 10
        range_end = range_start + 99
        return [
            member
            for member in SubServicesChoices
            if member in range(range_start, range_end + 1)
        ]


class SubServicesChoices(models.IntegerChoices):
    __empty__ = "Cap"

    # 1. Servei de mapeig i diagnosi
    MAP_DIAGNOSI_TAULA = 101, (
        "1 a  Taula territorial per l'articulació conjunta de l'economia "
        "social amb els diversos actors."
    )
    MAP_DIAGNOSI_CATALEG = 102, "1 b  Elaboració d'un catàleg bones pràctiques."
    MAP_DIAGNOSI_ORGANITZACIO = 103, (
        "1 c Organització de jornades, assistència a fires, actes i premis, "
        "trobades sectorials i col·laboracions."
    )
    MAP_DIAGNOSI_ALTRES = 199, (
        "1 d Altres accions dins del servei de mapeig i diagnosi."
    )

    # 2. Servei de divulgació, sensibilització i generació de coneixement
    DIV_SENS_GEN_CONEIXEMENT_CAMPANYA = 201, (
        "2 a Campanya de comunicació i difusió col·lectius especial atenció. "
        "Materials difusió fórmula cooperativa."
    )
    DIV_SENS_GEN_CONEIXEMENT_TALLERS = 202, (
        "2 b Tallers dirigits a joves estudiants de cicles formatius."
    )
    DIV_SENS_GEN_CONEIXEMENT_ACCIONS = 203, (
        "2 c Accions per a la creació de diferents classes de cooperatives."
    )
    DIV_SENS_GEN_CONEIXEMENT_DIAGNOSI = 204, (
        "2 d Diagnosi sobre les mancances i oportunitats socioeconòmiques i "
        "identificació empreses participants."
    )
    DIV_SENS_GEN_CONEIXEMENT_SESSIONS = 205, (
        "2 e Sessions col·lectives i d'acompanyament expert individual."
    )
    DIV_SENS_GEN_CONEIXEMENT_ALTRES = 299, (
        "2 f Altres accions dins del servei de divulgació, sensibilització i "
        "generació de coneixement."
    )

    # 3. Servei de Formació per a la promoció, creació i consolidació de
    # cooperatives i projectes d'ESS
    FORM_PROM_CREA_CONS_ACTIVITATS = 301, "3 a Accions formatives i informatives."
    FORM_PROM_CREA_CONS_FORMACIO = 302, (
        "3 b Tallers de formació bàsica a persones emprenedores interessades "
        "en la fòrmula cooperativa."
    )
    FORM_PROM_CREA_CONS_SESSIONS = 303, "3 c Sessions col·lectives."
    FORM_PROM_CREA_CONS_ACOMPANYAMENT = 304, "3 d Acompanyament expert."
    FORM_PROM_CREA_CONS_SENSIBILITZACIO = 305, (
        "3 e Tallers de sensibilització o dinamització adreçada al teixit "
        "associatiu, empreses o professionals."
    )
    FORM_PROM_CREA_CONS_ALTRES = 399, (
        "3 f Altres accions dins del servei de formació."
    )

    # 4. Servei d'acompanyament per a la creació i consolidació de cooperatives
    # i projectes d'ESS
    ACOM_CREA_CONS_CREACIO = 401, (
        "4 a Assessorament a mida per a la creació de cooperatives i altres "
        "organitzacions d'ESS."
    )
    ACOM_CREA_CONS_CONSOLIDACIO = 402, (
        "4 b Acompanyament a la consolidació i creixement de cooperatives "
        "existents."
    )
    ACOM_CREA_CONS_TRANSFORMACIO = 403, (
        "4 c Acompanyament a la transformació d'empreses."
    )
    ACOM_CREA_CONS_CAMPANYA = 404, "4 d Campanya de comunicació i difusió."
    ACOM_CREA_CONS_SENSIBILITZACIO = 405, (
        "4 e Accions de sensibilització o dinamització."
    )
    ACOM_CREA_CONS_ALTRES = 499, (
        "4 f Altres accions dins del servei d'acompanyament."
    )

    # 5. Servei de facilitació de la intercooperació, treball en xarxa i
    # dinamització territorial
    INTERCOOP_XARXA_TERRITORI_INTERCOOPERACIO = 501, (
        "5 a Generar espai d'intercooperació i treball en xarxa dins del "
        "territori."
    )
    INTERCOOP_XARXA_TERRITORI_INCORPORACIO = 502, (
        "5 b Incorporació d'empreses a l'ateneu cooperatiu i assemblea."
    )
    INTERCOOP_XARXA_TERRITORI_TREBALL = 503, (
        "5 c Treball en xarxa amb altres ateneus (reunions i iniciatives "
        "conjuntes)."
    )
    INTERCOOP_XARXA_TERRITORI_ALTRES = 599, (
        "5 d Altres accions dins del servei de facilitació."
    )

    # 6. Punt d'informació sobre l'ESS
    PUNT_INFO_ESPAI = 601, (
        "6 a  Espai físic per proporcional informació sobre ESS a diferents "
        "públics."
    )
    PUNT_INFO_DIFUSIO = 602, "6 b Difusió del punt o punts d'informació."

    # 7. Serveis complementaris
    SERV_COMPLEMENTARIS = 701, "7 a Serveis complementaris."


class CirclesChoices(models.IntegerChoices):
    __empty__ = "Cap"
    CERCLE0 = 0, "Ateneu"
    CERCLE1 = 1, "Cercle 1"
    CERCLE2 = 2, "Cercle 2"
    CERCLE3 = 3, "Cercle 3"
    CERCLE4 = 4, "Cercle 4"
    CERCLE5 = 5, "Cercle 5"

    @classmethod
    def choices_named(cls):
        if 'makemigrations' in sys.argv or 'migrate' in sys.argv:
            return cls.choices
        choices = [(None, cls.__empty__)] if hasattr(cls, "__empty__") else []
        for member in cls:
            if settings.CIRCLE_NAMES[member.value]:
                label = f"{member.label}: {settings.CIRCLE_NAMES[member.value]}"
            else:
                label = member.label
            choices.append((member.value, label))
        return choices

    @property
    def label_named(self):
        return (
            settings.CIRCLE_NAMES[self.value] if settings.CIRCLE_NAMES[self.value]
            else self.label
        )


class ActivityFileType(models.TextChoices):
    WORK = "WORK", "De treball"
    JUSTIFICATION = "JUSTIFICATION", "Justificatori"
