import re
from tagulous.models import TagField
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from tagulous.models import TagField
from django.contrib.auth import get_user_model

from apps.cc_users.managers import CCUserManager
from apps.cc_users.models import BaseUser
from apps.coopolis.storage_backends import PublicMediaStorage

from .general import Town
from django.core.validators import ValidationError
from localflavor.es.forms import ESIdentityCardNumberField
from apps.coopolis.choices import DocumentTypes
from apps.cc_users.constansts import PASSPORT_REGEX_PATTERNS


class User(BaseUser):
    class Meta:
        verbose_name = "persona"
        verbose_name_plural = "persones"
        ordering = ["-date_joined"]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CCUserManager()

    photo = models.FileField(
        "fotografia",
        storage=PublicMediaStorage(),
        max_length=250,
        blank=True,
        null=True,
        default="",
        help_text="Clica per carregar una imatge",
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "gif"])
        ],
    )
    fake_email = models.BooleanField(
        "e-mail inventat",
        default=False,
        help_text="Marca aquesta casella si el correu és inventat, i "
        "desmarca-la si mai el canvieu pel correu real. Ens ajudarà "
        "a mantenir la base de dades neta.",
    )
    username = models.CharField(
        unique=False, null=True, max_length=150, verbose_name="nom d'usuari/a"
    )
    username = models.CharField(unique=False, null=True, max_length=150,
                                verbose_name="nom d'usuari/a")
    surname2 = models.CharField("segon cognom", max_length=50, blank=True,
                                null=True)
    id_number_type = models.CharField("tipus de document", blank=True, null=True,
                                      choices=DocumentTypes.choices, max_length=10)
    id_number = models.CharField("DNI/NIE/Passaport", null=True, max_length=11, 
        help_text="Si degut a la teva situació legal et suposa un inconvenient"
        " indicar el DNI, deixa'l en blanc.")
    cannot_share_id = models.BooleanField(
        "Si degut a la teva situació legal et suposa un inconvenient"
        " indicar el DNI, deixa'l en blanc i marca aquesta casella",
        default=False,
    )
    GENDERS = (("OTHER", "Altre"), ("FEMALE", "Dona"), ("MALE", "Home"))
    gender = models.CharField(
        "gènere", blank=False, default="", choices=GENDERS, max_length=10
    )
    BIRTH_PLACES = (
        ("BARCELONA", "Barcelona"),
        ("CATALUNYA", "Catalunya"),
        ("ESPANYA", "Espanya"),
        ("OTHER", "Altre"),
    )
    birth_place = models.TextField(
        "lloc de naixement", blank=True, null=True, choices=BIRTH_PLACES
    )
    birthdate = models.DateField("data de naixement", blank=True, null=True)
    town = models.ForeignKey(
        Town,
        verbose_name="població actual",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )
    district = models.TextField(
        "districte", blank=True, null=True, choices=settings.DISTRICTS
    )
    address = models.CharField("adreça", max_length=250, blank=True, null=True)
    phone_number = models.CharField("telèfon", max_length=25, blank=True, null=True)
    STUDY_LEVELS = (
        ("MASTER", "Màster / Postgrau"),
        ("HIGH_SCHOOL", "Secundària"),
        ("WITHOUT_STUDIES", "Sense estudis"),
        ("FP", "Formació professional"),
        ("UNIVERSITY", "Estudis universitaris"),
        ("ELEMENTARY_SCHOOL", "Primària"),
    )
    educational_level = models.TextField(
        "nivell d'estudis", blank=True, null=True, choices=STUDY_LEVELS
    )
    EMPLOYMENT_OPTIONS = (
        ("SELF_EMPLOYED", "En actiu per compte propi"),
        ("UNEMPLOYMENT_BENEFIT_RECEIVER", "Perceptora de prestacions socials"),
        ("UNEMPLOYMENT_BENEFIT_REQUESTED", "Demandant d'ocupació"),
        ("EMPLOYED_WORKER", "En actiu per compte aliè"),
    )
    employment_situation = models.TextField(
        "situació laboral", blank=True, null=True, choices=EMPLOYMENT_OPTIONS
    )
    DISCOVERED_US_OPTIONS = (
        ("INTERNET", "Per internet i xarxes socials"),
        ("FRIEND", "A través d'un conegut"),
        ("PREVIOUS_ACTIVITY", "Per una activitat de l'ateneu"),
        ("OTHER", "Altres"),
    )
    discovered_us = models.TextField(
        "com ens has conegut", blank=True, null=True, choices=DISCOVERED_US_OPTIONS
    )
    project_involved = models.CharField(
        "si participes a un projecte cooperatiu o de l'ESS, indica'ns-el",
        blank=True,
        null=True,
        max_length=240,
    )
    cooperativism_knowledge = models.TextField(
        "coneixements previs",
        help_text="Tens coneixements / formació / experiència en "
        "cooperativisme? Quina? Cursos realitzats?",
        blank=True,
        null=True,
    )
    authorize_communications = models.BooleanField(
        "autoritza comunicació publicitària", default=False
    )
    tags = TagField(
        verbose_name="etiquetes",
        force_lowercase=True,
        blank=True,
        help_text="Prioritza les etiquetes que apareixen auto-completades. Si "
        "escrius una etiqueta amb un espai creurà que son dues "
        "etiquetes, per evitar-ho escriu-la entre cometes dobles, "
        '"etiqueta amb espais".',
    )

    @staticmethod
    def autocomplete_search_fields():
        filter_by = (
            "id__iexact",
            "email__icontains",
            "first_name__icontains",
            "id_number__contains",
            "last_name__icontains",
            "surname2__icontains",
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

    def check_id_number_in_database(self, id_number):
        model = get_user_model()
        if id_number and (
            model.objects
            .filter(id_number__iexact=id_number)
            .exclude(id=self.id)
            .exists()
        ):
            raise ValidationError({ 
                "id_number": ValidationError("El document ja existeix.") 
            })

    def _validate_passport(self, id_number):
        country_match = any(re.match(pattern, id_number) for pattern in PASSPORT_REGEX_PATTERNS)
        if not country_match:
            return { "id_number": ValidationError("Si us plau, introduïu un document vàlid.")}
        else:
            return {}
               
    def _validate_dni_nie(self, id_number):
        try: 
            ESIdentityCardNumberField().clean(id_number)
            return {}
        except ValidationError: 
            return { 
                "id_number": ValidationError("Si us plau, introduïu un document vàlid.") 
            }
        
    def clean(self):
        super().clean()
        errors = {}
        id_number_type = self.id_number_type
        id_number = self.id_number
        if not id_number_type:    
            errors.update({
                "id_number_type": ValidationError("Has de triar un tipus de document.")
            })
        if not id_number and id_number_type != DocumentTypes.NO_DNI:
            errors.update({
                "id_number": ValidationError("Aquest camp es obligatori.")
            })     
        elif id_number_type and id_number_type != DocumentTypes.NO_DNI:
            if id_number_type == DocumentTypes.PASSPORT:
                id_number_validation = errors.update(self._validate_passport(id_number))            
            else: 
                id_number_validation = errors.update(self._validate_dni_nie(id_number))
            if not id_number_validation:
                self.check_id_number_in_database(id_number)   
        
        if errors:
            raise ValidationError(errors)