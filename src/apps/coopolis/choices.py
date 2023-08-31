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
        "1 a Taula territorial per l'articulació conjunta de l'economia social "
        "amb els diversos actors (ATENEU)"
    )
    MAP_DIAGNOSI_CATALEG = 102, (
        "1 b Elaboració d'un catàleg bones pràctiques (ATENEU I CERCLES)"
    )
    MAP_DIAGNOSI_ORGANITZACIO = 103, (
        "1 c Organització de jornades per visibilitzar experiències, presència "
        "als mitjans de comunicació locals, assistència a fires, actes i "
        "premis, trobades sectorials, col·laboracions amb altres iniciatives "
        "(ATENEU)"
    )
    MAP_DIAGNOSI_ALTRES = 199, (
        "1 d Altres accions dins del servei de mapeig i diagnosi (ATENEU i "
        "CERCLES)"
    )
    MAP_DIAGNOSI_ACTES = 104, (
        "1 e Identificar actes, jornades, fires, programes i publicacions que "
        "ja s'estan duent a terme al territori on sigui interessant i factible "
        "la participació o la col·laboració de l'ateneu cooperatiu. (ATENEU)"
    )

    # 2. Servei de divulgació, sensibilització i generació de coneixement
    DIV_SENS_GEN_CONEIXEMENT_CAMPANYA = 201, (
        "2 a Campanya de comunicació i difusió a col·lectius especial atenció. "
        "Materials difusió fórmula cooperativa. (ATENEU)"
    )
    DIV_SENS_GEN_CONEIXEMENT_TALLERS = 202, (
        "2 b Tallers dirigits a joves estudiants de cicles formatius. (ATENEU)"
    )
    DIV_SENS_GEN_CONEIXEMENT_ACCIONS = 203, (
        "2 c Accions per a la creació de diferents classes de cooperatives. "
        "(CERCLES)"
    )
    DIV_SENS_GEN_CONEIXEMENT_DIAGNOSI = 204, (
        "2 d Diagnosi sobre les mancances i oportunitats socioeconòmiques i "
        "identificació de les empreses participants (CERCLES)"
    )
    DIV_SENS_GEN_CONEIXEMENT_SESSIONS = 205, (
        "2 e Sessions col·lectives i d'acompanyament expert individual. (CERCLES)"
    )
    DIV_SENS_GEN_CONEIXEMENT_ALTRES = 299, (
        "2 f Altres accions dins del servei de divulgació, sensibilització i "
        "generació de coneixement (ATENEU I CERCLES)"
    )
    DIV_SENS_GEN_CONEIXEMENT_DIFUSIO = 206, (
        "2 g Difusió materials (Ateneu)"
    )
    DIV_SENS_GEN_CONEIXEMENT_ELABORACIO = 207, (
        "2.h Elaboració material específic sobre la fórmula cooperativa (Ateneu)"
    )
    DIV_SENS_GEN_CONEIXEMENT_SENSIB = 208, (
        "2.i Accions de sensibilització"
    )

    # 3. Servei de Formació per a la promoció, creació i consolidació de
    # cooperatives i projectes d'ESS
    FORM_PROM_CREA_CONS_ACTIVITATS = 301, (
        "3 a Activitats formatives i informatives (ATENEU)"
    )
    FORM_PROM_CREA_CONS_FORMACIO = 302, (
        "3 b Tallers de formació bàsica a persones emprenedores interessades "
        "en la fòrmula cooperativa (ATENEU)"
    )
    FORM_PROM_CREA_CONS_SESSIONS = 303, "3 c Sessions col·lectives (ATENEU)"
    FORM_PROM_CREA_CONS_ACOMPANYAMENT = 304, "3 d Acompanyament expert (ATENEU)"
    FORM_PROM_CREA_CONS_SENSIBILITZACIO = 305, (
        "3 e Tallers de sensibilització o dinamització adreçada al teixit "
        "associatiu i a les empreses (ATENEU I CERCLES)"
    )
    FORM_PROM_CREA_CONS_ALTRES = 399, (
        "3 f Altres accions dins del servei de formació (ATENEU I CERCLES)"
    )
    FORM_PROM_CREA_CONS_TALLERS = 306, (
        "3 g Tallers de sensibilització o dinamització adreçada a "
        "professionals que s'agrupen (ATENEU I CERCLES)"
    )

    # 4. Servei d'acompanyament per a la creació i consolidació de cooperatives
    # i projectes d'ESS
    ACOM_CREA_CONS_CREACIO = 401, (
        "4 a Assessorament a mida per a la creació de cooperatives i altres "
        "organitzacions d'ESS (ATENEU i CERCLES)"
    )
    ACOM_CREA_CONS_CONSOLIDACIO = 402, (
        "4 b Acompanyament a la consolidació i creixement de cooperatives "
        "existents (ATENEU i CERCLES)"
    )
    ACOM_CREA_CONS_TRANSFORMACIO = 403, (
        "4 c Acompanyament a la transformació d'empreses ( ATENEU I CERCLES)"
    )
    ACOM_CREA_CONS_CAMPANYA = 404, (
        "4 d Campanya de comunicació i difusió (CERCLES)"
    )
    ACOM_CREA_CONS_SENSIBILITZACIO = 405, (
        "4 e Accions de sensibilització o dinamització (CERCLES)"
    )
    ACOM_CREA_CONS_ALTRES = 499, (
        "4 f Altres accions dins del servei d'acompanyament (ATENEU I CERCLES)"
    )

    # 5. Servei de facilitació de la intercooperació, treball en xarxa i
    # dinamització territorial
    INTERCOOP_XARXA_TERRITORI_INTERCOOPERACIO = 501, (
        "5 a Generar espais d'intercooperació i treball en xarxa dins del "
        "territori, intercooperació local, creació d'espais i grups "
        "d'intercooperació (ATENEU)"
    )
    INTERCOOP_XARXA_TERRITORI_INCORPORACIO = 502, (
        "5 b Incorporació d'empreses a l'ateneu cooperatiu (ATENEU)"
    )
    INTERCOOP_XARXA_TERRITORI_TREBALL = 503, (
        "5 c Treball en xarxa amb altres ateneus: assistir a reunions i "
        "col·laborar en iniciatives conjuntes (ATENEU)"
    )
    INTERCOOP_XARXA_TERRITORI_ALTRES = 599, (
        "5d Altres accions dins del servei d'intercooperació (ATENEU)"
    )
    INTERCOOP_XARXA_TERRITORI_ASS_ATENEU = 504, (
        "5e Assemblea ateneu "
    )
    INTERCOOP_XARXA_TERRITORI_ASS_XAC = 505, (
        "5f Assemblea XAC"
    )

    # 6. Punt d'informació sobre l'ESS
    PUNT_INFO_ESPAI = 601, (
        "6 a Espai físic per proporcionar informació sobre ESS a diferents "
        "públics (ATENEU I CERCLES)"
    )
    PUNT_INFO_DIFUSIO = 602, "6 b Punt o punts d'informació (ATENEU I CERCLES)"

    # 7. Serveis complementaris
    SERV_COMPLEMENTARIS = 701, "7 a Serveis Complementaris (ATENEU I CERCLES)"


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
