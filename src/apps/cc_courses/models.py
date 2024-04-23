import uuid
from datetime import date, datetime, time

from constance import config
from django.apps import apps
from django.conf import settings
from django.core.exceptions import NON_FIELD_ERRORS
from django.core.validators import ValidationError
from django.db import IntegrityError, models
from django.shortcuts import reverse
from django.utils import timezone
from easy_thumbnails.fields import ThumbnailerImageField

from apps.cc_courses.exceptions import EnrollToActivityNotValidException
from apps.cc_lib.utils import slugify_model
from apps.coopolis.choices import (
    ActivityFileType,
    CirclesChoices,
    ServicesChoices,
    SubServicesChoices,
)
from apps.coopolis.helpers import get_subaxis_choices, get_subaxis_for_axis
from apps.coopolis.managers import Published
from apps.coopolis.storage_backends import PrivateMediaStorage, PublicMediaStorage
from apps.dataexports.models import SubsidyPeriod
from conf.custom_mail_manager import MyMailTemplate


class CoursePlace(models.Model):
    class Meta:
        verbose_name = "lloc"
        ordering = [
            "name",
        ]

    name = models.CharField("nom", max_length=200, blank=False, unique=True)
    town = models.ForeignKey(
        "coopolis.Town",
        verbose_name="població",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    address = models.CharField("adreça", max_length=200)

    def __str__(self):
        return self.name


class Entity(models.Model):
    class Meta:
        verbose_name = "entitat"
        verbose_name_plural = "entitats"
        ordering = [
            "name",
        ]

    name = models.CharField("nom", max_length=200, blank=False, unique=True)
    legal_id = models.CharField("N.I.F.", max_length=9, blank=True, null=True)
    is_active = models.BooleanField(
        "Activa",
        default=True,
        help_text="Si la desactives no apareixerà al desplegable.",
    )

    def __str__(self):
        return self.name if self.is_active else f"[desactivada] {self.name}"


class Organizer(models.Model):
    class Meta:
        verbose_name = "organitzadora"
        verbose_name_plural = "organitzadores"
        ordering = ["name"]

    name = models.CharField("nom", max_length=200, blank=False, unique=True)

    def __str__(self):
        return self.name


class Cofunding(models.Model):
    class Meta:
        verbose_name = "cofinançadora"
        verbose_name_plural = "cofinançadores"
        ordering = [
            "name",
        ]

    name = models.CharField("nom", max_length=200, blank=False, unique=True, null=False)

    def __str__(self):
        return self.name


class StrategicLine(models.Model):
    class Meta:
        verbose_name = "línia estratègica"
        verbose_name_plural = "línies estratègiques"
        ordering = [
            "name",
        ]

    name = models.CharField("nom", max_length=200, blank=False, unique=True, null=False)

    def __str__(self):
        return self.name


class Course(models.Model):
    class Meta:
        verbose_name = "acció"
        verbose_name_plural = "accions"
        ordering = ["-date_start"]

    TYPE_CHOICES = (("F", "Accions educatives"), ("A", "Altres accions"))
    title = models.CharField("títol", max_length=250, blank=False)
    slug = models.CharField(max_length=250, unique=True)
    date_start = models.DateField("dia inici")
    date_end = models.DateField("dia finalització", null=True, blank=True)
    hours = models.CharField(
        "horaris",
        blank=False,
        max_length=200,
        help_text="Indica només els horaris, sense els dies.",
    )
    description = models.TextField("descripció", null=True)
    aimed_at = models.TextField("adreçat a", default="")
    publish = models.BooleanField("publicat")
    created = models.DateTimeField(
        "data de creació", null=True, blank=True, auto_now_add=True
    )
    banner = ThumbnailerImageField(
        null=True, storage=PublicMediaStorage(), max_length=250, blank=True
    )
    place = models.ForeignKey(
        CoursePlace,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="lloc",
        blank=True,
        help_text="Aquesta dada de moment és d'ús intern i no es publica.",
    )
    objects = models.Manager()
    published = Published()

    @classmethod
    def pre_save(cls, sender, instance, **kwargs):
        slugify_model(instance, "title")

    @property
    def absolute_url(self):
        if self.slug:
            return settings.ABSOLUTE_URL + reverse("course", args=[str(self.slug)])
        return None

    @staticmethod
    def autocomplete_search_fields():
        return ("title__icontains",)

    def __str__(self):
        return f"{self.title} ({self.date_start})"


class Activity(models.Model):
    class Meta:
        verbose_name = "sessió"
        verbose_name_plural = "sessions"
        ordering = ["-date_start"]

    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="acció",
        related_name="activities",
    )
    name = models.CharField("títol", max_length=200, blank=False, null=False)
    objectives = models.TextField("descripció", null=True)
    place = models.ForeignKey(
        CoursePlace, on_delete=models.SET_NULL, null=True, verbose_name="lloc"
    )
    date_start = models.DateField("dia inici")
    date_end = models.DateField("dia finalització", blank=True, null=True)
    starting_time = models.TimeField("hora d'inici")
    ending_time = models.TimeField("hora de finalització")
    confirmed = models.BooleanField(
        "confirmada",
        default=True,
        help_text="Per informació interna. No afecta la publicació.",
    )
    spots = models.IntegerField(
        "places totals",
        default=0,
        help_text="Si hi ha inscripcions en llista d'espera i augmentes el "
        "número de places, passaran a confirmades i se'ls hi "
        "notificarà el canvi. Si redueixes el número de places per "
        "sota del total d'inscrites les que ja estaven confirmades "
        "seguiran confirmades. Aquestes autotatitzacions únicament "
        "s'activen si la sessió té una data futura.",
    )
    enrolled = models.ManyToManyField(
        "coopolis.User",
        blank=True,
        related_name="enrolled_activities",
        verbose_name="inscrites",
        through="ActivityEnrolled",
    )
    circle = models.SmallIntegerField(
        "Ateneu / Cercle",
        choices=CirclesChoices.choices_named(),
        null=True,
        blank=True,
    )
    entity = models.ForeignKey(
        Entity, verbose_name="entitat", on_delete=models.SET_NULL, null=True, blank=True
    )
    organizer = models.ForeignKey(
        Organizer,
        verbose_name="organitzadora",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    responsible = models.ForeignKey(
        "coopolis.User",
        verbose_name="persona responsable",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="activities_responsible",
        help_text="Persona de l'equip al càrrec de la sessió. Per aparèixer "
        "al desplegable, cal que la persona tingui activada l'opció "
        "'Membre del personal'.",
    )
    exclude_from_justification = models.BooleanField(
        "No incloure a l'excel de justificació",
        default=False,
    )
    service = models.SmallIntegerField(
        "Servei",
        choices=ServicesChoices.choices,
        null=True,
        blank=True,
    )
    sub_service = models.SmallIntegerField(
        "Sub-servei",
        choices=SubServicesChoices.choices,
        null=True,
        blank=True,
    )
    axis = models.CharField(
        "(OBSOLET) Eix",
        help_text="Eix de la convocatòria on es justificarà.",
        choices=settings.AXIS_OPTIONS,
        null=True,
        blank=True,
        max_length=1,
    )
    subaxis = models.CharField(
        "(OBSOLET) Sub-eix",
        help_text="Correspon a 'Tipus d'acció' a la justificació.",
        null=True,
        blank=True,
        max_length=2,
        choices=get_subaxis_choices(),
    )
    photo1 = models.FileField(
        "fotografia",
        blank=True,
        null=True,
        storage=PrivateMediaStorage(),
        max_length=250,
    )
    photo3 = models.FileField(
        "fotografia 2",
        blank=True,
        null=True,
        storage=PrivateMediaStorage(),
        max_length=250,
    )
    photo2 = models.FileField(
        "document acreditatiu",
        blank=True,
        null=True,
        storage=PrivateMediaStorage(),
        max_length=250,
    )
    file1 = models.FileField(
        "material de difusió",
        blank=True,
        null=True,
        storage=PrivateMediaStorage(),
        max_length=250,
    )
    publish = models.BooleanField("publicada", default=True)
    # minors
    for_minors = models.BooleanField(
        "acció dirigida a menors",
        default=False,
        help_text="Determina el tipus de justificació i en aquest cas, s'han "
        "d'omplir els camps relatius a menors.",
    )
    minors_school_name = models.CharField(
        "nom del centre educatiu", blank=True, null=True, max_length=150
    )
    minors_school_cif = models.CharField(
        "CIF del centre educatiu", blank=True, null=True, max_length=12
    )
    MINORS_GRADE_OPTIONS = (
        ("PRIM", "Primària"),
        ("ESO", "Secundària obligatòria"),
        ("BATX", "Batxillerat"),
        ("FPGM", "Formació professional grau mig"),
        ("FPGS", "Formació professional grau superior"),
    )
    minors_grade = models.CharField(
        "grau d'estudis",
        blank=True,
        null=True,
        max_length=4,
        choices=MINORS_GRADE_OPTIONS,
    )
    minors_participants_number = models.IntegerField(
        "número d'alumnes participants", blank=True, null=True
    )
    minors_teacher = models.ForeignKey(
        "coopolis.User",
        on_delete=models.SET_NULL,
        verbose_name="docent",
        null=True,
        blank=True,
    )
    # room reservations module
    room_reservation = models.ForeignKey(
        apps.get_model("facilities_reservations", "Reservation", False),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="related_activities",
    )
    room = models.ForeignKey(
        apps.get_model("facilities_reservations", "Room", False),
        on_delete=models.SET_NULL,
        verbose_name="sala",
        related_name="activities",
        null=True,
        blank=True,
        help_text="Si selecciones una sala, quan guardis quedarà reservada "
        "per la sessió. <br>Consulta el "
        '<a href="/reservations/calendar/" target="_blank">'
        "CALENDARI DE RESERVES</a> per veure la disponibilitat.",
    )
    # cofunding options module
    cofunded = models.ForeignKey(
        Cofunding,
        verbose_name="Cofinançat",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cofunded_activities",
    )
    cofunded_ateneu = models.BooleanField(
        "Cofinançat amb Ateneus Cooperatius", default=False
    )
    strategic_line = models.ForeignKey(
        StrategicLine,
        verbose_name="línia estratègica",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="strategic_line_activities",
    )

    # Camps pel material formatiu
    videocall_url = models.URLField(
        "enllaç a la videotrucada", max_length=250, null=True, blank=True
    )
    instructions = models.TextField(
        "instruccions per participar",
        null=True,
        blank=True,
        help_text="Aquest text s'inclourà al correu de recordatori. És molt "
        "important que el formateig del text sigui el menor possible, i en"
        " particular, que si copieu i enganxeu el text d'algun altre lloc "
        'cap aquí, ho feu amb l\'opció "enganxar sense format", ja que '
        "sinó arrossegarà molta informació de formateig que "
        "probablement farà que el correu es vegi malament.",
    )
    poll_sent = models.DateTimeField(
        "data d'enviament de l'enquesta",
        null=True,
        blank=True,
    )
    organizer_reminded = models.DateTimeField(
        "data d'enviament de recordatori a responsable",
        null=True,
        blank=True,
    )

    # Camp per correu del recordatori d'omplir l'enquesta.
    poll_reminder_body = models.TextField(
        "Cos del correu de recordatori d'omplir l'enquesta",
        null=True,
        blank=True,
        help_text="Aquest text s'inclourà al correu de recordatori. És molt "
        "important que el formateig del text sigui el menor possible, i en"
        " particular, que si copieu i enganxeu el text d'algun altre lloc "
        'cap aquí, ho feu amb l\'opció "enganxar sense format", ja que '
        "sinó arrossegarà molta informació de formateig que "
        "probablement farà que el correu es vegi malament.",
    )
    equipments = models.ManyToManyField(
        to="facilities_reservations.Equipment",
        verbose_name="equipaments",
        blank=True,
    )
    teacher = models.CharField(
        "A càrrec de",
        max_length=50,
        default="",
        blank=True,
    )

    objects = models.Manager()
    published = Published()

    @property
    def remaining_spots(self):
        return self.spots - self.enrollments.filter(waiting_list=False).count()

    @property
    def waiting_list_count(self):
        return self.enrollments.filter(waiting_list=True).count()

    @property
    def waiting_list(self):
        return self.enrollments.filter(waiting_list=True).order_by("date_enrolled")

    @property
    def confirmed_enrollments(self):
        return self.enrollments.filter(waiting_list=False).order_by("date_enrolled")

    def user_is_confirmed(self, user):
        res = self.confirmed_enrollments.filter(user=user).all()
        return len(res) > 0

    @property
    def absolute_url(self):
        return self.course.absolute_url

    @property
    def is_past_due(self):
        return date.today() > self.date_start

    @property
    def datetime_start(self):
        if isinstance(self.date_start, date) and isinstance(self.starting_time, time):
            return datetime.combine(self.date_start, self.starting_time)
        return None

    @property
    def datetime_end(self):
        if not isinstance(self.ending_time, time):
            return None
        if not isinstance(self.date_end, date):
            if self.datetime_start:
                return datetime.combine(self.date_start, self.ending_time)
        return datetime.combine(self.date_end, self.ending_time)

    def axis_summary(self):
        axis = self.axis if self.axis else "(cap)"
        subaxis = self.subaxis if self.subaxis else "(cap)"
        return f"{axis} - {subaxis}"

    axis_summary.short_description = "Eix - Subeix"
    axis_summary.admin_order_field = "subaxis"

    @property
    def subsidy_period(self):
        if not self.date_start:
            return None
        model = apps.get_model("dataexports", "SubsidyPeriod")
        # Using date start as the reference one, if an activity last for more
        # than 1 day it should not matter here.
        obj = model.objects.get(
            date_start__lte=self.date_start, date_end__gte=self.date_start
        )
        return obj

    def poll_access_allowed(self):
        # Si la data actual és superior o igual a la data i hora d'inici,
        # mostrem  l'enquesta.
        naive_datetime = datetime.combine(self.date_start, self.starting_time)
        aware_datetime = timezone.make_aware(naive_datetime)
        if timezone.now() >= aware_datetime:
            return True
        return False

    def clean(self):
        """
        There's a necessary validation that cannot be included here so it must
        be done in corresponding forms' validations:
        To be able to select any equipments, Room must be selected as well.
        That way we make sure that a Reservation will always exist, to
        prevent Activities from reserving the same equipment as another
        Reservation.
        """
        super().clean()
        errors = {}
        if (
            self.minors_grade
            or self.minors_participants_number
            or self.minors_school_cif
            or self.minors_school_name
            or self.minors_teacher
        ):
            if not self.for_minors:
                errors.update(
                    {
                        "for_minors": ValidationError(
                            "Has omplert dades relatives a sessions "
                            "dirigides a menors però no has marcat "
                            "aquesta casella. Marca-la per tal que la "
                            "sessió es justifiqui com a tal."
                        ),
                    }
                )

        if self.axis:
            subaxis_options = get_subaxis_for_axis(str(self.axis))
            if self.subaxis not in subaxis_options:
                errors.update(
                    {
                        "subaxis": ValidationError(
                            "Has seleccionat un sub-eix que no es correspon a l'eix."
                        )
                    }
                )

        # Prevent using dates outside an existing subsidy period.
        if self.date_start and self.date_end:
            try:
                SubsidyPeriod.objects.get(
                    date_start__lte=self.date_start, date_end__gte=self.date_start
                )
            except SubsidyPeriod.DoesNotExist:
                errors.update(
                    {
                        "date_start": ValidationError(
                            "La data seleccionada correspon a una convocatòria "
                            "que no existeix a la base de dades."
                        )
                    }
                )

        # Prevents changing the date in a way that will change the subsidy
        # period in case there's an EmploymentInsertion linked to this Activity.
        if self.employment_insertions.exclude(
            subsidy_period=self.subsidy_period,
        ).count():
            msg = (
                "Aquesta sessió està vinculada a una inserció laboral de la "
                f"convocatòria {self.subsidy_period}, per aquest motiu no "
                "es pot indicar una data que caigui fora d'aquesta "
                "convocatòria."
            )
            errors.update({"date_start": ValidationError(msg)})

        # Excluding the activity from the justification excel while it has
        # empoyment insertions linked will most likely not be the desired
        # behaviour and will be difficult to detect, so we decided to make
        # the activity mandatory in the justification in that case.
        if (
            hasattr(self, "employment_insertions")
            and self.employment_insertions.count()
            and self.exclude_from_justification
        ):
            msg = (
                "Aquest sessió està vinculada a (com a mínim) una inserció "
                "laboral, per aquest motiu no es pot excloure de la "
                "justificació."
            )
            errors.update({"exclude_from_justification": ValidationError(msg)})

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.name

    def enroll_user(self, user):
        if user in self.enrolled.all():
            raise EnrollToActivityNotValidException()
        self.enrolled.add(user)
        self.save()

    def get_poll_email(self, user):
        mail = MyMailTemplate("EMAIL_ENROLLMENT_POLL")
        mail.subject_strings = {"activitat_nom": self.name}
        absolute_url_activity = ""
        if self.resources.exists():
            absolute_url_activity = settings.ABSOLUTE_URL + reverse("my_activities")
            absolute_url_activity = (
                "Descàrrega del material formatiu: <a "
                f'href="{absolute_url_activity}">Fitxa de la sessió</a>.'
            )
        absolute_url_poll = settings.ABSOLUTE_URL + reverse(
            "activity_poll", kwargs={"uuid": self.uuid}
        )
        poll_reminder_body = self.poll_reminder_body or ""
        poll_reminder_body = poll_reminder_body.replace("\n", "<br />")
        mail.body_strings = {
            "activitat_nom": self.name,
            "ateneu_nom": config.PROJECT_FULL_NAME,
            "persona_nom": user.first_name,
            "activitat_data_inici": self.date_start.strftime("%d-%m-%Y"),
            "activitat_hora_inici": self.starting_time.strftime("%H:%M"),
            "activitat_lloc": self.place,
            "absolute_url_activity": absolute_url_activity,
            "absolute_url_poll": absolute_url_poll,
            "absolute_url_my_activities": f"{settings.ABSOLUTE_URL}{reverse('my_activities')}",
            "url_web_ateneu": config.PROJECT_WEBSITE_URL,
            "poll_reminder_body": poll_reminder_body,
        }
        return mail

    def send_poll_email(self):
        enrollments = self.confirmed_enrollments
        for enrollment in enrollments:
            if enrollment.user.fake_email:
                continue
            mail = self.get_poll_email(enrollment.user)
            mail.send_to_user(enrollment.user)
        self.poll_sent = datetime.now()
        self.save()

    def get_reminder_to_responsible_email(self):
        mail = MyMailTemplate("EMAIL_ACTIVITY_RESPONSIBLE_REMINDER")
        mail.subject_strings = {
            "number_days": settings.REMIND_SESSION_ORGANIZER_DAYS_BEFORE,
            "activity_name": self.name,
        }
        absolute_url_admin_activity = settings.ABSOLUTE_URL + reverse(
            "admin:cc_courses_activity_change",
            kwargs={"object_id": self.id},
        )
        mail.body_strings = {
            "absolute_url_admin_activity": absolute_url_admin_activity,
        }
        return mail

    def send_reminder_to_responsible(self):
        mail = self.get_reminder_to_responsible_email()
        mail.send_to_user(self.responsible)
        self.organizer_reminded = datetime.now()
        self.save()

    @property
    def admin_url(self):
        if not self.id:
            return ""
        return reverse(
            "admin:cc_courses_activity_change",
            kwargs={"object_id": self.id},
        )

    @staticmethod
    def autocomplete_search_fields():
        return ("name__icontains",)


class ActivityResourceFile(models.Model):
    class Meta:
        verbose_name = "recurs"
        verbose_name_plural = "recursos i material formatiu"
        ordering = ["name"]

    image = models.FileField("fitxer", storage=PublicMediaStorage())
    name = models.CharField("nom del recurs", max_length=120, null=False, blank=False)
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, related_name="resources"
    )

    def __str__(self):
        return self.name


class ActivityFile(models.Model):
    class Meta:
        verbose_name = "fitxer"
        verbose_name_plural = "fitxers i enllaços interns"
        ordering = ["name"]

    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, related_name="files"
    )
    file = models.FileField(
        "fitxer adjunt",
        storage=PrivateMediaStorage(),
        blank=True,
        null=True,
    )
    file_type = models.CharField(
        "tipus de fitxer",
        choices=ActivityFileType.choices,
        max_length=50,
    )
    url = models.URLField(
        "fitxer enllaçat",
        blank=True,
        null=True,
    )
    name = models.CharField(
        "nom del fitxer",
        max_length=120,
        null=False,
        blank=False,
        help_text="Pensa un nom prou descriptiu com perquè ajudi a altres "
        "persones a preparar possibles requeriments d'aquí uns mesos o anys.",
    )

    def __str__(self):
        return self.name

    def clean(self):
        errors = {}
        if self.file and self.url:
            errors.update(
                {
                    "file": ValidationError(
                        "No pots incloure un fitxer adjunt si també inclous "
                        "un fitxer enllaçat."
                    ),
                    "url": ValidationError(
                        "No pots incloure un fitxer enllaçat si també inclous "
                        "un fitxer adjunt."
                    ),
                }
            )
        if not self.file and not self.url:
            errors.update(
                {
                    NON_FIELD_ERRORS: ValidationError(
                        "Cal indicar un fitxer ja sigui adjunt o enllaçat."
                    ),
                }
            )
        if errors:
            raise ValidationError(errors)


class ActivityEnrolled(models.Model):
    class Meta:
        db_table = "cc_courses_activity_enrolled"
        unique_together = ("user", "activity")
        verbose_name = "inscripció"
        verbose_name_plural = "inscripcions"

    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        verbose_name="sessió",
        related_name="enrollments",
    )
    user = models.ForeignKey(
        "coopolis.User",
        on_delete=models.CASCADE,
        verbose_name="persona",
        related_name="enrollments",
    )
    date_enrolled = models.DateTimeField(
        "data d'inscripció", auto_now_add=True, null=True
    )
    user_comments = models.TextField("comentaris", null=True, blank=True)
    waiting_list = models.BooleanField("en llista d'espera", default=False)
    reminder_sent = models.DateTimeField("Recordatori enviat", null=True, blank=True)

    def can_access_poll(self):
        if self.waiting_list or not self.activity.poll_access_allowed():
            return False
        return True

    def can_access_details(self):
        if not self.waiting_list and (
            self.activity.videocall_url
            or self.activity.instructions
            or len(self.activity.resources.all()) > 0
        ):
            return True
        return False

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):

        # Aquí hi feia un "if not self.id", de manera que l'actualització de
        # waiting_list només passava a les inscripcions noves, i provocava que
        # al canviar el nº d'spots, les que ja estaven en llista d'espera no
        # passessin a confirmades.
        if not self.activity.is_past_due:
            is_full = self.activity.remaining_spots < 1
            self.waiting_list = is_full

        try:
            super(ActivityEnrolled, self).save(
                force_insert, force_update, using, update_fields
            )
        except IntegrityError as e:
            if "duplicate" in str(e):
                raise ValidationError(
                    {
                        NON_FIELD_ERRORS: "Ja tens inscripció a aquesta activitat.",
                    }
                )
            raise e

    def send_confirmation_email(self):
        mail = MyMailTemplate("EMAIL_ENROLLMENT_CONFIRMATION")
        mail.subject_strings = {"activitat_nom": self.activity.name}
        mail.body_strings = {
            "activitat_nom": self.activity.name,
            "ateneu_nom": config.PROJECT_FULL_NAME,
            "activitat_data_inici": self.activity.date_start.strftime("%d-%m-%Y"),
            "activitat_hora_inici": self.activity.starting_time.strftime("%H:%M"),
            "activitat_lloc": self.activity.place,
            "absolute_url_my_activities": f"{settings.ABSOLUTE_URL}{reverse('my_activities')}",
            "url_web_ateneu": config.PROJECT_WEBSITE_URL,
        }
        mail.send_to_user(self.user)

    def send_waiting_list_email(self):
        mail = MyMailTemplate("EMAIL_ENROLLMENT_WAITING_LIST")
        mail.subject_strings = {"activitat_nom": self.activity.name}
        mail.body_strings = {
            "activitat_nom": self.activity.name,
            "ateneu_nom": config.PROJECT_FULL_NAME,
            "activitat_data_inici": self.activity.date_start.strftime("%d-%m-%Y"),
            "activitat_hora_inici": self.activity.starting_time.strftime("%H:%M"),
            "activitat_lloc": self.activity.place,
            "url_els_meus_cursos": f"{settings.ABSOLUTE_URL}{reverse('my_activities')}",
            "url_ateneu": settings.ABSOLUTE_URL,
        }
        mail.send_to_user(self.user)

    @staticmethod
    def get_reminder_email(user, activity):
        mail = MyMailTemplate("EMAIL_ENROLLMENT_REMINDER")
        mail.subject_strings = {"activitat_nom": activity.name}
        absolute_url_activity = settings.ABSOLUTE_URL + reverse("my_activities")
        mail.body_strings = {
            "activitat_nom": activity.name,
            "ateneu_nom": config.PROJECT_FULL_NAME,
            "persona_nom": user.first_name,
            "activitat_data_inici": activity.date_start.strftime("%d-%m-%Y"),
            "activitat_hora_inici": activity.starting_time.strftime("%H:%M"),
            "activitat_lloc": activity.place,
            "activitat_instruccions": activity.instructions,
            "absolute_url_activity": absolute_url_activity,
            "absolute_url_my_activities": f"{settings.ABSOLUTE_URL}{reverse('my_activities')}",
            "url_web_ateneu": config.PROJECT_WEBSITE_URL,
        }
        return mail

    def send_reminder_email(self):
        mail = self.get_reminder_email(self.user, self.activity)
        mail.send_to_user(self.user)
        self.reminder_sent = datetime.now()
        self.save()

    def __str__(self):
        return f"Inscripció de {self.user.full_name} a: {self.activity.name}"
