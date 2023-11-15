import re
from tagulous.models import TagField
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

from apps.cc_users.managers import CCUserManager
from apps.cc_users.models import BaseUser
from .general import Town
from django.core.validators import ValidationError
from django.core.exceptions import NON_FIELD_ERRORS
from localflavor.es.forms import ESIdentityCardNumberField
from apps.coopolis.choices import DocumentTypes


class User(BaseUser):
    class Meta:
        verbose_name = "persona"
        verbose_name_plural = "persones"
        ordering = ["-date_joined"]

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CCUserManager()

    fake_email = models.BooleanField(
        "e-mail inventat", default=False,
        help_text="Marca aquesta casella si el correu és inventat, i "
                  "desmarca-la si mai el canvieu pel correu real. Ens ajudarà "
                  "a mantenir la base de dades neta."
    )
    username = models.CharField(unique=False, null=True, max_length=150,
                                verbose_name="nom d'usuari/a")
    surname2 = models.CharField("segon cognom", max_length=50, blank=True,
                                null=True)

    id_number_type = models.CharField("tipus de document", blank=True, null=True, choices=DocumentTypes.choices, max_length=10)
    id_number = models.CharField("DNI/NIE/Passaport", null=True, max_length=11, 
        help_text="Si degut a la teva situació legal et suposa un inconvenient"
        " indicar el DNI, deixa'l en blanc.") #TODO: Validar texto.
    cannot_share_id = models.BooleanField(
        "Si degut a la teva situació legal et suposa un inconvenient"
        " indicar el DNI, deixa'l en blanc i marca aquesta casella",
        default=False,
    )
    GENDERS = (
        ('OTHER', 'Altre'),
        ('FEMALE', 'Dona'),
        ('MALE', 'Home')
    )
    gender = models.CharField("gènere", blank=True, null=True, choices=GENDERS,
                              max_length=10)
    BIRTH_PLACES = (
        ("BARCELONA", "Barcelona"),
        ("CATALUNYA", "Catalunya"),
        ("ESPANYA", "Espanya"),
        ("OTHER", "Altre")
    )
    birth_place = models.TextField("lloc de naixement", blank=True, null=True,
                                   choices=BIRTH_PLACES)
    birthdate = models.DateField("data de naixement", blank=True, null=True)
    town = models.ForeignKey(Town, verbose_name="població actual",
                             on_delete=models.SET_NULL, null=True, blank=False)
    district = models.TextField("districte", blank=True, null=True,
                                choices=settings.DISTRICTS)
    address = models.CharField("adreça", max_length=250, blank=True, null=True)
    phone_number = models.CharField("telèfon", max_length=25, blank=True,
                                    null=True)
    STUDY_LEVELS = (
        ('MASTER', 'Màster / Postgrau'),
        ('HIGH_SCHOOL', 'Secundària'),
        ('WITHOUT_STUDIES', 'Sense estudis'),
        ('FP', 'Formació professional'),
        ('UNIVERSITY', 'Estudis universitaris'),
        ('ELEMENTARY_SCHOOL', 'Primària')
    )
    educational_level = models.TextField("nivell d'estudis", blank=True,
                                         null=True, choices=STUDY_LEVELS)
    EMPLOYMENT_OPTIONS = (
        ('SELF_EMPLOYED', 'En actiu per compte propi'),
        ('UNEMPLOYMENT_BENEFIT_RECEIVER', 'Perceptora de prestacions socials'),
        ('UNEMPLOYMENT_BENEFIT_REQUESTED', "Demandant d'ocupació"),
        ('EMPLOYED_WORKER', 'En actiu per compte aliè')
    )
    employment_situation = models.TextField(
        "situació laboral", blank=True, null=True, choices=EMPLOYMENT_OPTIONS)
    DISCOVERED_US_OPTIONS = (
        ('INTERNET', 'Per internet i xarxes socials'),
        ('FRIEND', "A través d'un conegut"),
        ('PREVIOUS_ACTIVITY', "Per una activitat de l'ateneu"),
        ('OTHER', 'Altres')
    )
    discovered_us = models.TextField("com ens has conegut", blank=True,
                                     null=True, choices=DISCOVERED_US_OPTIONS)
    project_involved = models.CharField(
        "si participes a un projecte cooperatiu o de l'ESS, indica'ns-el",
        blank=True, null=True, max_length=240)
    cooperativism_knowledge = models.TextField(
        "coneixements previs",
        help_text="Tens coneixements / formació / experiència en "
                  "cooperativisme? Quina? Cursos realitzats?",
        blank=True, null=True
    )
    authorize_communications = models.BooleanField(
        "autoritza comunicació publicitària", default=False)
    tags = TagField(
        verbose_name="etiquetes",
        force_lowercase=True, blank=True,
        help_text="Prioritza les etiquetes que apareixen auto-completades. Si "
                  "escrius una etiqueta amb un espai creurà que son dues "
                  "etiquetes, per evitar-ho escriu-la entre cometes dobles, "
                  "\"etiqueta amb espais\"."
    )

    @staticmethod
    def autocomplete_search_fields():
        filter_by = (
            "id__iexact", "email__icontains", "first_name__icontains",
            "id_number__contains", "last_name__icontains",
            "surname2__icontains"
        )
        return filter_by

    def enrolled_activities_count(self):
        return self.enrolled_activities.all().count()

    enrolled_activities_count.short_description = "Sessions"

    @property
    def project(self):
        if self.projects.count() > 0:
            return self.projects.all()[0]
        return None

    def get_full_name(self):
        name = self.first_name
        if self.surname:
            name = f"{name} {self.surname}"
        return name

    @property
    def full_name(self):
        return self.get_full_name()

    @property
    def surname(self):
        surname = None
        if self.last_name:
            surname = self.last_name
        if self.surname2:
            if surname:
                surname = f"{surname} {self.surname2}"
            else:
                surname = self.surname2
        return surname

    def __str__(self):
        return self.get_full_name()

    def clean(self):
        super().clean()
        errors = {}
        id_number_type = self.id_number_type
        id_number = self.id_number

        if not id_number_type:    
            errors.update({
                "id_number_type": ValidationError("Has de triar un tipus de document.")
            })
        elif id_number_type != DocumentTypes.NO_DNI:
            validate_id_number = True
            if id_number_type == DocumentTypes.PASSPORT:
                passport_regex_patterns = [
                    r'^[A-Z]{2}\d{7}$',  # ARMENIA (AM)
                    r'^[A-Z]{3}\d{6}$',  # ARGENTINA (AR)
                    r'^[A-Z]\d{7}$',  # AUSTRIA (AT)
                    r'^[A-Z]\d{7}$',  # AUSTRALIA (AU)
                    r'^[A-Z]{2,3}\d{7,8}$',  # AZERBAIJAN (AZ)
                    r'^[A-Z]{2}\d{6}$',  # BELGIUM (BE)
                    r'^\d{9}$',  # BULGARIA (BG)
                    r'^[A-Z]{2}\d{6}$',  # BRAZIL (BR)
                    r'^[A-Z]{2}\d{7}$',  # BELARUS (BY)
                    r'^[A-Z]{2}\d{6}$',  # CANADA (CA)
                    r'^[A-Z]\d{7}$',  # SWITZERLAND (CH)
                    r'^G\d{8}$|^E(?![IO])[A-Z0-9]\d{7}$',  # CHINA (CN)
                    r'^[A-Z](\d{6}|\d{8})$',  # CYPRUS (CY)
                    r'^\d{8}$',  # CZECH REPUBLIC (CZ)
                    r'^[CFGHJKLMNPRTVWXYZ0-9]{9}$',  # GERMANY (DE)
                    r'^\d{9}$',  # DENMARK (DK)
                    r'^\d{9}$',  # ALGERIA (DZ)
                    r'^([A-Z]\d{7}|[A-Z]{2}\d{7})$',  # ESTONIA (EE)
                    r'^[A-Z0-9]{2}([A-Z0-9]?)\d{6}$',  # SPAIN (ES)
                    r'^[A-Z]{2}\d{7}$',  # FINLAND (FI)
                    r'^\d{2}[A-Z]{2}\d{5}$',  # FRANCE (FR)
                    r'^\d{9}$',  # UNITED KINGDOM (GB)
                    r'^[A-Z]{2}\d{7}$',  # GREECE (GR)
                    r'^\d{9}$',  # CROATIA (HR)
                    r'^[A-Z]{2}(\d{6}|\d{7})$',  # HUNGARY (HU)
                    r'^[A-Z0-9]{2}\d{7}$',  # IRELAND (IE)
                    r'^[A-Z]{1}-?\d{7}$',  # INDIA (IN)
                    r'^[A-C]\d{7}$',  # INDONESIA (ID)
                    r'^[A-Z]\d{8}$',  # IRAN (IR)
                    r'^(A)\d{7}$',  # ICELAND (IS)
                    r'^[A-Z0-9]{2}\d{7}$',  # ITALY (IT)
                    r'^[Aa]\d{7}$',  # JAMAICA (JM)
                    r'^[A-Z]{2}\d{7}$',  # JAPAN (JP)
                    r'^[MS]\d{8}$',  # SOUTH KOREA (KR)
                    r'^[a-zA-Z]\d{7}$',  # KAZAKHSTAN (KZ)
                    r'^[a-zA-Z]\d{5}$',  # LIECHTENSTEIN (LI)
                    r'^[A-Z0-9]{8}$',  # LITHUANIA (LT)
                    r'^[A-Z0-9]{8}$',  # LUXEMBURG (LU)
                    r'^[A-Z0-9]{2}\d{7}$',  # LATVIA (LV)
                    r'^[A-Z0-9]{8}$',  # LIBYA (LY)
                    r'^\d{7}$',  # MALTA (MT)
                    r'^([A-Z]{2}\d{7})|(\d{2}[A-Z]{2}\d{5})$',  # MOZAMBIQUE (MZ)
                    r'^[AHK]\d{8}$',  # MALAYSIA (MY)
                    r'^\d{10,11}$',  # MEXICO (MX)
                    r'^[A-Z]{2}[A-Z0-9]{6}\d$',  # NETHERLANDS (NL)
                    r'^([Ll]([Aa]|[Dd]|[Ff]|[Hh])|[Ee]([Aa]|[Pp])|[Nn])\d{6}$',  # NEW ZEALAND (NZ)
                    r'^([A-Z](\d{6}|\d{7}[A-Z]))|([A-Z]{2}(\d{6}|\d{7}))$',  # PHILIPPINES (PH)
                    r'^[A-Z]{2}\d{7}$',  # PAKISTAN (PK)
                    r'^[A-Z]{2}\d{7}$',  # POLAND (PL)
                    r'^[A-Z]\d{6}$',  # PORTUGAL (PT)
                    r'^\d{8,9}$',  # ROMANIA (RO)
                    r'^\d{9}$',  # RUSSIAN FEDERATION (RU)
                    r'^\d{8}$',  # SWEDEN (SE)
                    r'^(P)[A-Z]\d{7}$',  # SLOVENIA (SL)
                    r'^[0-9A-Z]\d{7}$',  # SLOVAKIA (SK)
                    r'^[A-Z]{1,2}\d{6,7}$',  # THAILAND (TH)
                    r'^[A-Z]\d{8}$',  # TURKEY (TR)
                    r'^[A-Z]{2}\d{6}$',  # UKRAINE (UA)
                    r'^\d{9}$',  # UNITED STATES (US)
                    r'^[TAMD]\d{8}$',  # SOUTH AFRICA (ZA)
                ]
                for pattern in passport_regex_patterns:
                    if re.match(pattern, id_number):
                        country_match = True
                        break
                if not country_match:
                    errors.update({
                        "id_number": ValidationError("Si us plau, introduïu un passaport vàlid.")
                    })
                    validate_id_number = False
            else: 
                try: 
                    ESIdentityCardNumberField().clean(id_number)
                except: 
                    errors.update({
                        "id_number": ValidationError(f"Si us plau, introduïu un {id_number_type} vàlid.")
                    })
                    validate_id_number = False

            if validate_id_number:
                model = get_user_model()
                if id_number and (
                    model.objects
                    .filter(id_number__iexact=id_number)
                    .exclude(id=self.id)
                    .exists()
                ):
                    errors.update({
                        "id_number_type": ValidationError(f"El {DocumentTypes[id_number_type].label} ja existeix.")
                    })     
        
        if errors:
            raise ValidationError(errors)
