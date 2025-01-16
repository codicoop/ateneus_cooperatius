import datetime

import tagulous.models
from constance import config
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Q, Sum
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.timezone import now

from apps.cc_courses.choices import ProjectStageStatesChoices, StageTypeChoices
from apps.cc_courses.models import Cofunding, Entity, Organizer, StrategicLine
from apps.coopolis.choices import CirclesChoices, ServicesChoices, SubServicesChoices
from apps.coopolis.helpers import get_subaxis_choices, get_subaxis_for_axis
from apps.coopolis.models import Town, User
from apps.coopolis.storage_backends import PrivateMediaStorage, PublicMediaStorage
from apps.dataexports.models import SubsidyPeriod
from conf.post_office import send


class Derivation(models.Model):
    class Meta:
        verbose_name = "derivació"
        verbose_name_plural = "derivacions"
        ordering = ["name"]

    name = models.CharField("nom", max_length=250)

    def __str__(self):
        return self.name


class Project(models.Model):
    class Meta:
        verbose_name_plural = "projectes"
        verbose_name = "projecte"

    partners = models.ManyToManyField(
        "User", verbose_name="sòcies", blank=True, related_name="projects"
    )
    logo = models.FileField(
        "imatge del projecte",
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
    name = models.CharField("nom", max_length=200, blank=False, unique=True)
    SECTORS = (
        ("M", "Alimentació"),
        ("S", "Assessorament"),
        ("A", "Altres"),
        ("C", "Comunicació i tecnologia"),
        ("CU", "Cultura"),
        ("U", "Cures"),
        ("E", "Educació"),
        ("F", "Finances"),
        ("H", "Habitatge"),
        ("L", "Logística"),
        ("O", "Oci"),
        ("R", "Roba"),
    )
    sector = models.CharField(max_length=2, choices=SECTORS)
    web = models.CharField("Web", max_length=200, blank=True)
    PROJECT_STATUS_OPTIONS = (
        ("IN_MEDITATION_PROCESS", "En proces de debat/reflexió"),
        ("IN_CONSTITUTION_PROCESS", "En constitució"),
        ("RUNNING", "Constituïda"),
        ("DOWN", "Caigut"),
    )
    project_status = models.CharField(
        "estat del projecte",
        max_length=50,
        blank=True,
        null=True,
        choices=PROJECT_STATUS_OPTIONS,
    )
    MOTIVATION_OPTIONS = (
        ("COOPERATIVISM_EDUCATION", "Formació en cooperativisme"),
        ("COOPERATIVE_CREATION", "Constitució d'una cooperativa"),
        ("TRANSFORM_FROM_ASSOCIATION", "Transformació d'associació a cooperativa"),
        ("TRANSFORM_FROM_SCP", "Transformació de SCP a cooperativa"),
        ("ENTERPRISE_RELIEF", "Relleu empresarial"),
        ("CONSOLIDATION", "Consolidació"),
        ("OTHER", "Altres"),
    )
    motivation = models.CharField(
        "petició inicial",
        max_length=50,
        blank=True,
        null=True,
        choices=MOTIVATION_OPTIONS,
    )
    mail = models.EmailField("correu electrònic")
    phone = models.CharField("telèfon", max_length=25)
    town = models.ForeignKey(
        Town, verbose_name="població", on_delete=models.SET_NULL, null=True, blank=True
    )
    district = models.TextField(
        "districte", blank=True, null=True, choices=settings.DISTRICTS
    )
    number_people = models.IntegerField("número de persones", blank=True, null=True)
    registration_date = models.DateField(
        "data de registre", blank=True, null=True, default=datetime.date.today
    )
    cif = models.CharField("N.I.F.", max_length=11, blank=True, null=True)
    object_finality = models.TextField("objecte i finalitat", blank=True, null=True)
    project_origins = models.TextField("orígens del projecte", blank=True, null=True)
    solves_necessities = models.TextField(
        "quines necessitats resol el vostre projecte?", blank=True, null=True
    )
    social_base = models.TextField(
        "compta el vostre projecte amb una base social?", blank=True, null=True
    )
    constitution_date = models.DateField("data de constitució", blank=True, null=True)
    estatuts = models.FileField(
        "estatuts", blank=True, null=True, storage=PrivateMediaStorage(), max_length=250
    )
    viability = models.FileField(
        "pla de viabilitat",
        blank=True,
        null=True,
        storage=PrivateMediaStorage(),
        max_length=250,
    )
    sostenibility = models.FileField(
        "pla de sostenibilitat",
        blank=True,
        null=True,
        storage=PrivateMediaStorage(),
        max_length=250,
    )
    derivation = models.ForeignKey(
        Derivation,
        verbose_name="derivat",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    derivation_date = models.DateField("data de derivació", blank=True, null=True)
    description = models.TextField("descripció", blank=True, null=True)
    other = models.CharField(
        "altres",
        max_length=240,
        blank=True,
        null=True,
        help_text="Apareix a la taula de Seguiment d'Acompanyaments",
    )
    employment_estimation = models.PositiveIntegerField(
        "insercions laborals previstes", default=0
    )
    follow_up_situation = models.CharField(
        "seguiment",
        max_length=50,
        choices=settings.PROJECT_STATUS,
        blank=True,
        null=True,
    )
    follow_up_situation_update = models.DateTimeField(
        "actualització seguiment", blank=True, null=True
    )
    tags = tagulous.models.TagField(
        verbose_name="etiquetes",
        force_lowercase=True,
        blank=True,
        help_text="Prioritza les etiquetes que apareixen auto-completades. Si "
        "escrius una etiqueta amb un espai creurà que son dues "
        "etiquetes, per evitar-ho escriu-la entre cometes dobles, "
        '"etiqueta amb espais".',
    )
    is_draft = models.BooleanField(
        default=False,
    )

    @property
    def has_estatus(self):
        if self.estatuts:
            return True
        else:
            return False

    @property
    def has_viability(self):
        if self.viability:
            return True
        else:
            return False

    @property
    def has_sostenibility(self):
        if self.sostenibility:
            return True
        else:
            return False

    @property
    def stages_list(self):
        if not self.stages or self.stages.count() < 1:
            return None
        stages = []
        for stage in self.stages.all():
            name = stage.get_stage_type_display()
            if stage.stage_subtype:
                name = f"{name} ({stage.stage_subtype.name})"
            stages.append(name)
        stages.sort()
        return "; ".join(stages)

    @property
    def axis_list(self):
        """
        Justification export prior to 1/11/2021 still use this method as will
        probably do so forever unless they decide to completely ditch the
        information about axis and subaxis.
        """
        if not self.stages or self.stages.count() < 1:
            return None
        stages = []
        for stage in self.stages.all():
            stages.append(stage.axis_summary())
        stages.sort()
        return "; ".join(stages)

    @property
    def services_list(self):
        if not self.stages or self.stages.count() < 1:
            return None
        stages = [
            stage.get_service_display() for stage in self.stages.all() if stage.service
        ]
        return "; ".join(stages)

    @property
    def last_stage_responsible(self):
        if not self.stages or self.stages.count() < 1:
            return None
        return self.stages.all()[0].stage_responsible

    last_stage_responsible.fget.short_description = "Últim acompanyament"

    @property
    def last_stage_circle(self):
        if not self.stages or self.stages.count() < 1:
            return None
        return self.stages.all()[0].get_circle_display()

    last_stage_circle.fget.short_description = "Cercle de l'últim acompanyament"

    @property
    def full_town_district(self):
        if not self.town:
            return None
        ret = self.town
        if self.district:
            ret = f"{ret} ({self.get_district_display()})"
        return ret

    @property
    def follow_up_with_date(self):
        if self.follow_up_situation_update:
            date = self.follow_up_situation_update.strftime("%d-%m-%Y")
            return f"{self.follow_up_situation} ({date})"
        return self.follow_up_situation

    @staticmethod
    def autocomplete_search_fields():
        return ("name__icontains",)

    @property
    def partners_activities(self):
        acts = []
        for partner in self.partners.all():
            for activity in partner.enrolled_activities.all():
                if activity not in acts:
                    activity = f"{activity.date_start}: {activity}"
                    acts.append(activity)
        acts.sort()
        return mark_safe("<br>".join(acts))

    partners_activities.fget.short_description = "Sessions"

    @property
    def partners_participants(self):
        """
        To display the list of all the people who participated in project
        stage sessions.
        """
        if not self.id:
            return "-"
        participants = User.objects.filter(
            stage_sessions_participated__project_stage__project=self,
        ).distinct()
        participants_strings = [str(x) for x in participants]
        participants_strings.sort()
        return mark_safe(", ".join(participants_strings))

    partners_participants.fget.short_description = (
        "Participants a sessions d'acompanyament"
    )

    def save(self, *args, **kw):
        if self.pk is not None:
            orig = Project.objects.get(pk=self.pk)
            if orig.follow_up_situation != self.follow_up_situation:
                self.follow_up_situation_update = now()
        super(Project, self).save(*args, **kw)

    def notify_new_request_to_ateneu(self):
        context = {
            "projecte_nom": self.name,
            "projecte_telefon": self.phone,
            "projecte_email": self.mail,
            "usuari_email": self.partners.all()[0].email,
        }
        send(
            recipients=config.EMAIL_FROM_PROJECTS.split(","),
            template="EMAIL_NEW_PROJECT",
            context=context,
        )

    def notify_request_confirmation(self):
        context = {
            "projecte_nom": self.name,
            "url_backoffice": settings.ABSOLUTE_URL,
        }
        send(
            recipients=self.partners.all()[0].email,
            template="EMAIL_PROJECT_REQUEST_CONFIRMATION",
            context=context,
        )

    def __str__(self):
        return self.name


class StageSubtype(models.Model):
    class Meta:
        verbose_name = "subtipus"
        verbose_name_plural = "subtipus"

    name = models.CharField("nom", max_length=200, blank=False, unique=True, null=False)

    def __str__(self):
        return self.name


class ProjectFile(models.Model):
    class Meta:
        verbose_name = "fitxer"
        verbose_name_plural = "fitxers"
        ordering = ["name"]

    image = models.FileField("fitxer", storage=PublicMediaStorage(), max_length=250)
    name = models.CharField(
        "Etiqueta",
        max_length=250,
        null=False,
        blank=False,
        help_text="Els fitxers antics tenen com a etiqueta el propi nom de "
        "l'arxiu, però aquí hi pot anar qualsevol text descriptiu.",
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="files")

    def __str__(self):
        return self.name


class ProjectStage(models.Model):
    class Meta:
        verbose_name = "justificació d'acompanyament"
        verbose_name_plural = "justificacions d'acompanyaments"
        ordering = ["-date_start"]

    DEFAULT_STAGE_TYPE = 1

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        verbose_name="projecte acompanyat",
        related_name="stages",
    )
    stage_state = models.CharField(
        "estat de l'acompanyament",
        max_length=8,
        choices=ProjectStageStatesChoices.choices,
        null=True,
        blank=True,
        default=None,
    )
    stage_type = models.CharField(
        "tipus d'acompanyament",
        max_length=2,
        default=DEFAULT_STAGE_TYPE,
        choices=StageTypeChoices.choices,
    )
    stage_subtype = models.ForeignKey(
        StageSubtype,
        verbose_name="subtipus",
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    subsidy_period = models.ForeignKey(
        SubsidyPeriod, verbose_name="convocatòria", null=True, on_delete=models.SET_NULL
    )
    exclude_from_justification = models.BooleanField(
        "No incloure a l'excel de justificació",
        default=False,
    )
    date_start = models.DateField(
        "data creació acompanyament", null=False, blank=False, auto_now_add=True
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
    circle = models.SmallIntegerField(
        "Ateneu / Cercle",
        choices=CirclesChoices.choices_named(),
        null=True,
        blank=True,
    )
    # Entity was called "organizer" before, causing confusion, specially
    # because we wanted to add the Organizer field
    # here. We renamed 'organizer' to entity and made a migration for this
    # change (0046_auto...py).
    # Then I added the 'organizer' FK field. Makemigration worked fine, but
    # migrate was throwing an error:
    #   django.db.utils.ProgrammingError: relation
    #   "coopolis_projectstage_organizer_id_26459182" already exists
    # In the database everything was correct, not a field or a key in
    # coopolis_projectstage table called 'organizer'
    # or any other reference, also not postgres cache glitches or anything I
    # could identify.
    # Did the experiment of calling it differently and worked.
    # Given that I don't understand the problem, leaving the field with a
    # different name seems the safest option.
    stage_organizer = models.ForeignKey(
        Organizer,
        verbose_name="organitzadora",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    stage_responsible = models.ForeignKey(
        "User",
        verbose_name="persona responsable",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="stage_responsible",
        help_text="Persona de l'equip al càrrec de l'acompanyament. Per "
        "aparèixer al desplegable, cal que la persona tingui "
        "activada la opció 'Membre del personal'.",
    )
    scanned_certificate = models.FileField(
        "Certificat",
        blank=True,
        null=True,
        storage=PrivateMediaStorage(),
        max_length=250,
    )
    involved_partners = models.ManyToManyField(
        User,
        verbose_name="(obsolet) Persones involucrades",
        blank=True,
        related_name="stage_involved_partners",
        help_text="Persones que apareixeran a la justificació com a que han "
        "participat a l'acompanyament.",
    )

    # cofunding options module
    cofunded = models.ForeignKey(
        Cofunding,
        verbose_name="Cofinançat",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cofunded_projects",
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
        related_name="strategic_line_projects",
    )

    def axis_summary(self):
        axis = self.axis if self.axis else "(cap)"
        subaxis = self.subaxis if self.subaxis else "(cap)"
        return f"{axis}-{subaxis}"

    axis_summary.short_description = "Eix - Subeix"
    axis_summary.admin_order_field = "axis"

    def hours_sum(self):
        total_qs = self.stage_sessions.aggregate(total_sum=Sum("hours"))
        total = 0 if not total_qs["total_sum"] else total_qs["total_sum"]
        return total

    hours_sum.short_description = "Suma d'hores"

    def sessions_count(self):
        return len(self.stage_sessions.all())

    sessions_count.short_description = "Nº sessions"

    def clean(self):
        super().clean()
        errors = {}
        if self.axis:
            subaxis_options = get_subaxis_for_axis(str(self.axis))
            if self.subaxis not in subaxis_options:
                errors.update(
                    {
                        "subaxis": ValidationError(
                            "Has seleccionat un sub-eix que no es " "correspon a l'eix."
                        )
                    }
                )

        if self.stage_state == ProjectStageStatesChoices.OPEN:
            open_project_stages = ProjectStage.objects.filter(
                project=self.project,
                stage_state=ProjectStageStatesChoices.OPEN,
            ).exclude(id=self.id)

            if open_project_stages.count():
                errors.update(
                    {
                        "stage_state": ValidationError(
                            "No es pot tenir més d'un acompanyament en procés."
                        )
                    }
                )

        if self.stage_state == ProjectStageStatesChoices.PENDING:
            if (
                self.project.stages.filter(
                    stage_state=ProjectStageStatesChoices.PENDING
                )
                .exclude(id=self.id)
                .exists()
            ):
                errors.update(
                    {
                        "stage_state": ValidationError(
                            "Aquest projecte ja té un acompanyament sol·licitat."
                        )
                    }
                )

        if errors:
            raise ValidationError(errors)

    def get_full_type_str(self):
        txt = self.get_stage_type_display()
        if config.ENABLE_STAGE_SUBTYPES and self.stage_subtype:
            txt = f"{txt} ({self.stage_subtype.name})"
        return txt

    @property
    def latest_session(self):
        try:
            return self.stage_sessions.latest("date")
        except ProjectStageSession.DoesNotExist:
            return None

    @property
    def earliest_session(self):
        try:
            return self.stage_sessions.earliest("date")
        except ProjectStageSession.DoesNotExist:
            return None

    @property
    def involved_partners_count(self):
        return self.partners_involved_in_sessions.count()

    @property
    def partners_involved_in_sessions(self):
        return User.objects.filter(
            stage_sessions_participated__in=self.stage_sessions.all()
        ).distinct()

    @property
    def justification_documents_total(self):
        docs_count = self.stage_sessions.exclude(
            Q(justification_file="") | Q(justification_file=None),
        ).count()
        return f"{docs_count} / {self.stage_sessions.count()}"

    justification_documents_total.fget.short_description = "Docs justif."

    @property
    def entities_str(self):
        sessions = self.stage_sessions.filter(entity__isnull=False).distinct("entity")
        entities_list = [str(x.entity) for x in sessions]
        entities_list.sort()
        return ", ".join(entities_list)

    def __str__(self):
        txt = (
            f"{str(self.project)}: {self.get_full_type_str()} "
            f"[{str(self.subsidy_period)}]"
        )
        return txt

    @staticmethod
    def autocomplete_search_fields():
        return (
            "project__id__iexact",
            "project__name__icontains",
        )


class ProjectStageSession(models.Model):
    class Meta:
        verbose_name = "Sessió d'acompanyament"
        verbose_name_plural = "Sessions d'acompanyament"

    project_stage = models.ForeignKey(
        ProjectStage,
        on_delete=models.CASCADE,
        related_name="stage_sessions",
        verbose_name="justificació d'acompanyament",
    )
    session_responsible = models.ForeignKey(
        "User",
        verbose_name="persona facilitadora",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="stage_sessions",
        help_text="Persona de l'equip que ha facilitat la sessió. Per "
        "aparèixer al desplegable, cal que la persona tingui "
        "activada la opció 'Membre del personal'.",
    )
    date = models.DateField("data", default=datetime.date.today, null=True, blank=False)
    hours = models.FloatField(
        "número d'hores",
        help_text="Camp necessari per la justificació.",
        null=True,
        blank=True,
    )
    follow_up = models.TextField("seguiment", null=True, blank=True)
    # Aquest camp Entity no apareix enlloc, pendent que confirmin si és correcte que no hi ha de ser
    # per marcar-lo com a obsolet o bé ja eliminar-lo.
    entity = models.ForeignKey(
        Entity,
        verbose_name="Entitat",
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    involved_partners = models.ManyToManyField(
        User,
        verbose_name="persones involucrades",
        blank=True,
        related_name="stage_sessions_participated",
        help_text="Persones que apareixeran a la justificació com a que han "
        "participat a la sessió d'acompanyament.",
    )
    justification_file = models.FileField(
        "fitxer de justificació",
        storage=PrivateMediaStorage(),
        blank=True,
        null=True,
    )
    # Information showed to the project partners
    objective = models.TextField("objectiu de la sessió", blank=True, null=True)
    result = models.TextField("retorn", blank=True, null=True)
    file1 = models.FileField(
        "material adjunt",
        blank=True,
        null=True,
        storage=PublicMediaStorage(),
        max_length=250,
    )
    file2 = models.FileField(
        "", blank=True, null=True, storage=PublicMediaStorage(), max_length=250
    )
    file3 = models.FileField(
        "", blank=True, null=True, storage=PublicMediaStorage(), max_length=250
    )

    @property
    def project_partners(self):
        partners = self.project_stage.project.partners.all()
        partners_list = [str(x) for x in partners]
        partners_list.sort()
        return ", ".join(partners_list)

    project_partners.fget.short_description = "Persones sòcies"

    def __str__(self):
        return (
            f"Sessió d'acompanyament del {self.date} per "
            f"{self.project_stage.project.name}"
        )


class ProjectsFollowUp(Project):
    """
    Deprecated: from Nov 2021 this is kept to let them access older reports,
    but when they don't need them anymore this and the corresponding admin view
    and template can be deleted.
    """

    class Meta:
        proxy = True
        verbose_name_plural = "(obsolet) Seguiment d'acompanyaments per eix"
        verbose_name = "(obsolet) Seguiment d'acompanyament per eix"
        ordering = ["follow_up_situation", "follow_up_situation_update"]


class ProjectsFollowUpService(Project):
    class Meta:
        proxy = True
        verbose_name_plural = "Seguiment d'acompanyaments"
        verbose_name = "Seguiment d'acompanyament"
        ordering = ["follow_up_situation", "follow_up_situation_update"]


class EmploymentInsertion(models.Model):
    class Meta:
        verbose_name = "inserció laboral"
        verbose_name_plural = "insercions laborals"
        ordering = ["-insertion_date"]

    project = models.ForeignKey(
        Project,
        on_delete=models.PROTECT,
        verbose_name="projecte acompanyat",
        related_name="employment_insertions",
        blank=True,
        null=True,
    )
    activity = models.ForeignKey(
        "cc_courses.Activity",
        verbose_name="sessió",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="employment_insertions",
    )
    user = models.ForeignKey(
        User, verbose_name="persona", blank=True, null=True, on_delete=models.PROTECT
    )
    subsidy_period = models.ForeignKey(
        SubsidyPeriod, verbose_name="convocatòria", null=True, on_delete=models.SET_NULL
    )
    insertion_date = models.DateField("alta seguretat social")
    end_date = models.DateField("baixa seg. social", null=True, blank=True)
    CONTRACT_TYPE_CHOICES = (
        (1, "Indefinit"),
        (5, "Temporal"),
        (2, "Formació i aprenentatge"),
        (3, "Pràctiques"),
        (4, "Soci/a cooperativa o societat laboral"),
    )
    contract_type = models.SmallIntegerField(
        "tipus de contracte", choices=CONTRACT_TYPE_CHOICES, null=True
    )
    circle = models.SmallIntegerField(
        "Ateneu / Cercle",
        choices=CirclesChoices.choices_named(),
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.user.full_name}: {self.get_contract_type_display()}"

    @classmethod
    def validate_extended_fields(
        cls, user_obj, project_obj, activity_obj, subsidy_period, link_to_project=True
    ):
        if not isinstance(user_obj, User):
            raise ValidationError(
                {"user": ValidationError("Aquest camp és obligatori.")}
            )

        user_errors = cls.get_user_field_errors(user_obj)
        cif_error = cls.get_project_cif_field_errors(
            project_obj,
            link_to_project,
        )
        activity_subsidy_period_error = cls.get_activity_field_errors(
            activity_obj,
            subsidy_period,
        )
        activity_excluded_error = cls.get_activity_excluded_error(activity_obj)

        errors = []
        if user_errors:
            errors.append(ValidationError(user_errors))
        if cif_error:
            errors.append(ValidationError(cif_error))
        if activity_subsidy_period_error:
            errors.append(ValidationError(activity_subsidy_period_error))
        if activity_excluded_error:
            errors.append(ValidationError(activity_excluded_error))

        if errors:
            raise ValidationError(errors)

    @classmethod
    def get_activity_excluded_error(cls, activity_obj):
        msg = ""
        if activity_obj and activity_obj.exclude_from_justification:
            url = reverse(
                "admin:cc_courses_activity_change",
                kwargs={"object_id": activity_obj.id},
            )
            a_tag = f'<a href="{url}" target="_blank">fitxa de l\'activitat</a>'
            msg = (
                "L'activitat seleccionada no és vàlida perquè està exclosa de "
                "l'exportació de la justificació. Per poder vincular insercions"
                f" laborals a aquesta activitat, cal que aneu a la {a_tag} i "
                f"hi desactiveu el camp 'No incloure a l'excel de justificació'."
            )
        return mark_safe(msg)

    @staticmethod
    def get_user_field_errors(user_obj):
        user_errors = []
        msg = ""
        if isinstance(user_obj, User):
            user_obj_errors = {
                "surname": "- Cognom.<br />",
                "gender": "- Gènere. <br/>",
                "birthdate": "- Data de naixement.<br />",
                "birth_place": "- Lloc de naixement.<br />",
                "town": "- Municipi.<br />",
            }
            user_errors = [
                value
                for key, value in user_obj_errors.items()
                if not getattr(user_obj, key)
            ]
        if user_errors:
            user_url = reverse(
                "admin:coopolis_user_change", kwargs={"object_id": user_obj.id}
            )
            url = f'<a href="{user_url}" target="_blank">Fitxa de la Persona</a>'
            msg += (
                f"No s'ha pogut desar la inserció laboral. Hi ha camps de "
                f"la fitxa de la persona que normalment son opcionals, "
                f"però que per poder justificar les insercions laborals "
                f"son obligatoris.<br>"
                f"De la {url}:<br /> {''.join(user_errors)}<br />"
            )
        return mark_safe(msg)

    @staticmethod
    def get_project_cif_field_errors(project_obj, link_to_project):
        msg = ""
        if isinstance(project_obj, Project) and not project_obj.cif:
            url = "fitxa del Projecte (en aquest mateix formulari, més amunt)"
            if link_to_project:
                project_url = reverse(
                    "admin:coopolis_project_change",
                    kwargs={"object_id": project_obj.id},
                )
                url = f'<a href="{project_url}" target="_blank">fitxa del Projecte</a>'
            msg += (
                f"No s'ha pogut desar la inserció laboral. Hi ha camps del "
                f"Projecte que normalment son opcionals, "
                f"però que per poder justificar les insercions laborals "
                f"son obligatoris.<br>"
                f"De la {url}:<br>"
                f"- NIF.<br>"
            )
        return mark_safe(msg)

    @staticmethod
    def get_activity_field_errors(activity_obj, subsidy_period):
        msg = ""
        if activity_obj and activity_obj.subsidy_period != subsidy_period:
            msg = (
                "L'activitat seleccionada no és vàlida perquè té una "
                "convocatòria diferent que la indicada en aquesta inserció "
                "laboral."
            )
        return mark_safe(msg)

    @staticmethod
    def validate_activity_project(activity_obj, project_obj):
        errors = []
        if not activity_obj and not project_obj:
            msg = "Un dels camps 'Projecte acompanyat' o 'Sessió' és obligatori."
            errors.append(ValidationError(msg))
        if activity_obj and project_obj:
            msg = "Només es pot triar un camp entre 'Projecte acompanyat' o 'Sessió'."
            errors.append(ValidationError(msg))
        if errors:
            raise ValidationError(errors)


class CreatedEntity(models.Model):
    project_stage = models.OneToOneField(
        ProjectStage,
        verbose_name="Acompanyament vinculat a la creació de l'entitat",
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        related_name="created_entity",
    )
    project = models.ForeignKey(
        Project,
        verbose_name="(Obsolet) Projecte",
        on_delete=models.CASCADE,
        related_name="created_entities",
        null=True,
    )
    service = models.SmallIntegerField(
        "(Obsolet) Servei",
        choices=ServicesChoices.choices,
        null=True,
    )
    sub_service = models.SmallIntegerField(
        "(Obsolet) Sub-servei",
        choices=SubServicesChoices.choices,
        null=True,
    )
    subsidy_period = models.ForeignKey(
        SubsidyPeriod,
        verbose_name="(Obsolet) Convocatòria de la constitució",
        null=True,
        on_delete=models.SET_NULL,
    )
    circle = models.SmallIntegerField(
        "(Obsolet) Ateneu / Cercle",
        choices=CirclesChoices.choices_named(),
        null=True,
    )
    entity = models.ForeignKey(
        Entity,
        verbose_name="(Obsolet) Entitat",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = "Entitat creada"
        verbose_name_plural = "Entitats creades"

    def __str__(self):
        if self.project_stage:
            return f"Entitat creada: {self.project_stage.project.name}"
        if self.project:
            return f"Entitat creada: {self.project.name}"
        return "Entitat creada sense projecte ni acompanyament assignat."

    @classmethod
    def validate_extended_fields(cls, project_stage_obj):
        if not isinstance(project_stage_obj, ProjectStage):
            return True
        project_obj = project_stage_obj.project
        project_obj_errors = {
            "cif": "- NIF.<br />",
            "constitution_date": "- Data de constitució. <br/>",
        }
        project_errors = [
            value
            for key, value in project_obj_errors.items()
            if not getattr(project_obj, key)
        ]

        if not project_errors:
            return True
        project_url = reverse(
            "admin:coopolis_project_change", kwargs={"object_id": project_obj.id}
        )
        url = f'<a href="{project_url}" target="_blank">fitxa del Projecte</a>'
        msg = (
            f"No s'ha pogut desar l'entitat creada. Hi ha camps del "
            f"Projecte que normalment son opcionals, "
            f"però que per poder justificar les entitats creades "
            f"son obligatoris.<br>"
        )
        msg += f"De la {url}:<br /> {''.join(project_errors)}<br />"
        raise ValidationError(mark_safe(msg))


class ProjectsConstitutedService(CreatedEntity):
    class Meta:
        proxy = True
        verbose_name_plural = "Projectes constituïts"
        verbose_name = "Projecte constituït"
