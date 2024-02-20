from datetime import datetime

from constance import config
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm
from django.core.exceptions import ValidationError
from django.db.models import BLANK_CHOICE_DASH
from django.forms import models
from django.utils.safestring import mark_safe
from django.utils.timezone import make_aware

from apps.cc_courses.models import Activity, ActivityEnrolled
from apps.coopolis.mixins import FormDistrictValidationMixin
from apps.coopolis.models import ActivityPoll, EmploymentInsertion, Project, User
from apps.coopolis.models.projects import CreatedEntity
from apps.coopolis.widgets import XDSoftDatePickerInput
from apps.facilities_reservations.models import Reservation, ReservationEquipment


class ProjectForm(FormDistrictValidationMixin, forms.ModelForm):
    required_css_class = "required"

    class Meta:
        model = Project
        fields = (
            "logo",
            "name",
            "town",
            "sector",
            "district",
            "mail",
            "web",
            "phone",
            "estatuts",
            "viability",
            "sostenibility",
        )
        exclude = (
            "cif",
            "registration_date",
            "constitution_date",
        )

    fieldsets = [
        (
            None,
            {"fields": ("logo",)},
        ),
        (
            None,
            {
                "fields": (
                    "name",
                    "town",
                    "sector",
                    "district",
                    "mail",
                    "web",
                    "phone",
                )
            },
        ),
        (
            None,
            {
                "fields": (
                    "estatus",
                    "viability",
                    "sostenibility",
                )
            },
        ),
    ]


class ProjectStageStartForm(FormDistrictValidationMixin, forms.ModelForm):
    required_css_class = "required"

    class Meta:
        model = Project
        fields = (
            "name",
            "town",
            "sector",
            "district",
            "mail",
            "phone",
            "object_finality",
        )


class ProjectStageAttachForm(FormDistrictValidationMixin, forms.ModelForm):
    required_css_class = "required"

    class Meta:
        model = Project
        fields = (
            "estatuts",
            "viability",
            "sostenibility",
        )


class ProjectStageInitialPetitionForm(FormDistrictValidationMixin, forms.ModelForm):
    required_css_class = "required"

    class Meta:
        model = Project
        fields = (
            "project_status",
            "motivation",
        )


class ProjectCharacteristicsForm(FormDistrictValidationMixin, forms.ModelForm):
    required_css_class = "required"

    class Meta:
        model = Project
        fields = (
            "project_origins",
            "solves_necessities",
            "social_base",
        )


class ProjectFormAdmin(ProjectForm):
    class Meta:
        # Un-excluding the fields that we were hiding for the front-end.
        exclude = None

    def clean(self):
        super().clean()
        if EmploymentInsertion.objects.filter(
            project=self.instance.id,
        ).count():
            msg = (
                "Aquest projecte està vinculat a insercions laborals, "
                "per aquest motiu, aquest camp és obligatori."
            )
            if not self.cleaned_data.get("cif"):
                self.add_error("cif", msg)
        if CreatedEntity.objects.filter(
            project=self.instance.id,
        ).count():
            msg = (
                "Aquest projecte està vinculat a una creació d'entitat, "
                "per aquest motiu, aquest camp és obligatori."
            )
            if not self.cleaned_data.get("cif"):
                self.add_error("cif", msg)
            if not self.cleaned_data.get("constitution_date"):
                self.add_error("constitution_date", msg)
        return self.cleaned_data


class EmploymentInsertionInlineFormSet(models.BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            if not hasattr(form, "cleaned_data"):
                continue
            data = form.cleaned_data
            if "DELETE" not in data:
                # When there are no rows in the formset it still calls this
                # clean() but with empty data.
                continue
            # Skipping the ones marked for deletion:
            if data["DELETE"]:
                continue
            # We're checking for all the rows because trying to check only
            # for new ones will cause problems, as we'll need to check also
            # for rows in which the user has been modified (or make the
            # user row read only when editing).
            # New (unsaved yet) ones will have data['id'] == None
            EmploymentInsertion.validate_extended_fields(
                data["user"],
                data["project"],
                False,
            )


class EmploymentInsertionAdminForm(models.ModelForm):
    class Meta:
        model = EmploymentInsertion
        fields = (
            "project",
            "user",
            "subsidy_period",
            "insertion_date",
            "end_date",
            "contract_type",
            "circle",
        )

    def clean(self):
        super().clean()
        EmploymentInsertion.validate_extended_fields(
            self.cleaned_data.get("user"),
            self.cleaned_data.get("project"),
        )
        return self.cleaned_data


class MySignUpForm(FormDistrictValidationMixin, UserCreationForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "email",
            "last_name",
            "phone_number",
            "surname2",
            "birthdate",
            "id_number",
            "birth_place",
            "cannot_share_id",
            "town",
            "gender",
            "address",
            "educational_level",
            "discovered_us",
            "employment_situation",
            "project_involved",
            "password1",
            "password2",
            "authorize_communications",
        )

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "surname2",
                    "email",
                    "id_number",
                    "cannot_share_id",
                    "phone_number",
                    "birthdate",
                    "birth_place",
                    "town",
                    "district",
                    "address",
                    "gender",
                )
            },
        ),
        (
            "Explican'ns més de tu",
            {
                "fields": (
                    "educational_level",
                    "discovered_us",
                    "employment_situation",
                    "project_involved",
                )
            },
        ),
        (
            None,
            {
                "fields": (
                    "password1",
                    "password2",
                    "authorize_communications",
                )
            },
        ),
    ]

    required_css_class = "required"
    first_name = forms.CharField(label="Nom", max_length=30)
    last_name = forms.CharField(label="Cognom", max_length=30, required=True)
    email = forms.EmailField(label="Correu electrònic", max_length=254)
    birthdate = forms.DateField(
        label="Data de naixement", required=True, widget=XDSoftDatePickerInput()
    )
    accept_conditions = forms.BooleanField(label="He llegit i accepto", required=True)
    accept_conditions2 = forms.BooleanField(label="He llegit i accepto", required=True)
    authorize_communications = forms.BooleanField(
        label="Accepto rebre informació sobre els serveis", required=False
    )
    birth_place = forms.ChoiceField(
        label="Lloc de naixement",
        choices=[
            BLANK_CHOICE_DASH[0],
            ("CATALUNYA", "Catalunya"),
            ("ESPANYA", "Espanya"),
            ("OTHER", "Altre"),
        ],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["id_number"].required = False
        if "accept_conditions" in self.fields:
            self.fields["accept_conditions"].help_text = mark_safe(
                config.CONTENT_SIGNUP_LEGAL1
            )
        if "accept_conditions2" in self.fields:
            self.fields["accept_conditions2"].help_text = mark_safe(
                config.CONTENT_SIGNUP_LEGAL2
            )
        self.label_suffix = ""

    def clean(self):
        super().clean()
        cannot_share_id = self.cleaned_data.get("cannot_share_id")
        id_number = self.cleaned_data.get("id_number")
        if not id_number and not cannot_share_id:
            msg = (
                "Necessitem el DNI, NIF o passaport per justificar la "
                "participació davant dels organismes públics que financen "
                "aquestes activitats."
            )
            self.add_error("id_number", msg)
        return self.cleaned_data

    def clean_id_number(self):
        model = get_user_model()
        value = self.cleaned_data.get("id_number")
        if value and model.objects.filter(id_number__iexact=value).exists():
            raise ValidationError("El DNI ja existeix.")
        return value


class MySignUpAdminForm(FormDistrictValidationMixin, forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "surname2",
            "id_number",
            "email",
            "phone_number",
            "birthdate",
            "birth_place",
            "town",
            "district",
            "address",
            "gender",
            "educational_level",
            "employment_situation",
            "discovered_us",
            "project_involved",
        )

    password = ReadOnlyPasswordHashField()
    new_password = forms.CharField(
        label="Canviar contrasenya",
        help_text=(
            "La contrasenya actual no es pot veure per seguretat. "
            "Però si escrius una contrasenya en aquest camp i deses els "
            "canvis, l'usuari passarà a tenir aquesta nova contrasenya. "
            "Mentre escrius, la contrasenya és visible per tal que puguis "
            "copiar-la i enviar-li a l'usuari."
        ),
        max_length=150,
        required=False,
    )
    first_name = forms.CharField(label="Nom", max_length=30)
    last_name = forms.CharField(label="Cognom", max_length=30, required=False)
    no_welcome_email = forms.BooleanField(
        label="No enviar correu de benvinguda",
        help_text="Al crear un compte per defecte s'enviarà un correu de"
        " notificació amb l'enllaç al back-office i instruccions. "
        "Si marqueu aquesta casella, no s'enviarà.",
        required=False,
    )
    resend_welcome_email = forms.BooleanField(
        label="Reenviar correu de benvinguda",
        required=False,
        help_text="Marca aquesta casella si desitges tornar a enviar la "
        "notificació de creació de nou compte.",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "town" in self.fields:
            self.fields["town"].required = False

        self.fields["id_number"].required = False

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        if "password" in self.initial:
            return self.initial["password"]
        return None

    def clean(self):
        super().clean()
        cannot_share_id = self.cleaned_data.get("cannot_share_id")
        id_number = self.cleaned_data.get("id_number")
        if not id_number and not cannot_share_id:
            msg = (
                "Necessitem el DNI, NIF o passaport per justificar la "
                "participació davant dels organismes públics que financen "
                "aquestes activitats."
            )
            self.add_error("id_number", msg)

        if EmploymentInsertion.objects.filter(
            user=self.instance.id,
        ).count():
            msg = (
                "Aquesta persona està vinculada a una inserció laboral, "
                "per aquest motiu, aquest camp és obligatori."
            )
            if not self.cleaned_data.get("last_name"):
                self.add_error("last_name", msg)
            if not self.cleaned_data.get("gender"):
                self.add_error("gender", msg)
            if not self.cleaned_data.get("birthdate"):
                self.add_error("birthdate", msg)
            if not self.cleaned_data.get("birth_place"):
                self.add_error("birth_place", msg)
            if not self.cleaned_data.get("town"):
                self.add_error("town", msg)
        return self.cleaned_data


def get_item_choices(model, value):
    choices = []

    item = sorted(settings.SUBAXIS_OPTIONS[value])

    for thing in item:
        choices.append(
            {
                "value": thing[0],
                "label": thing[1],
            }
        )

    return choices


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = (
            "course",
            "name",
            "objectives",
            "place",
            "date_start",
            "date_end",
            "starting_time",
            "ending_time",
            "spots",
            "enrolled",
            "entity",
            "organizer",
            "axis",
            "subaxis",
            "photo1",
            "photo2",
            "publish",
            "for_minors",
            "minors_school_name",
            "minors_school_cif",
            "minors_grade",
            "minors_participants_number",
            "minors_teacher",
            "room",
            "equipments",
            "confirmed",
        )

    def clean(self):
        super().clean()
        if self.cleaned_data["room"]:
            self.validate_room_availability()
        if not self.cleaned_data.get("room") and self.cleaned_data.get("equipments"):
            self.add_error(
                "equipments",
                "Per reservar equipaments cal seleccionar "
                "també una Sala que estigui disponible.",
            )
        return self.cleaned_data

    def validate_room_availability(self):
        date_end = self.cleaned_data["date_start"]
        if self.cleaned_data["date_end"]:
            date_end = self.cleaned_data["date_end"]
        id = self.instance.room_reservation_id
        values = {
            "id": id,
            "title": "foo",
            "start": make_aware(
                datetime.combine(
                    self.cleaned_data["date_start"], self.cleaned_data["starting_time"]
                )
            ),
            "end": make_aware(
                datetime.combine(date_end, self.cleaned_data["ending_time"])
            ),
            "room": self.cleaned_data["room"],
        }
        reservation_obj = Reservation(**values)
        try:
            reservation_obj.clean()
        except ValidationError as e:
            self.add_error(None, e)

        for equipment in self.cleaned_data["equipments"]:
            equipment_obj = ReservationEquipment(
                reservation=reservation_obj,
                equipment=equipment,
            )
            try:
                equipment_obj.clean()
            except ValidationError as e:
                if "equipment" in e.message_dict:
                    self.add_error(
                        "equipments",
                        f"L'equipament {equipment.name} no està disponible en "
                        "aquest horari.",
                    )
                else:
                    self.add_error(None, e)


class ActivityEnrolledForm(forms.ModelForm):
    class Meta:
        model = ActivityEnrolled
        fields = ("user",)

    send_enrollment_email = forms.BooleanField(
        label="Enviar notificació d'inscripció",
        required=False,
        help_text="Si fas una inscripció des del panell d'administració, per "
        "defecte no s'envia el correu. Marca aquesta casella per "
        "tal que el rebi de la mateixa manera que si s'hagués "
        "inscrit des de la part pública.",
    )


class ActivityPollForm(forms.ModelForm):
    class Meta:
        model = ActivityPoll
        fields = (
            # Organització
            "duration",
            "hours",
            "information",
            "on_schedule",
            "included_resources",
            "space_adequation",
            # Continguts
            "contents",
            # Metodologia
            "methodology_fulfilled_objectives",
            "methodology_better_results",
            "participation_system",
            # Valoració de la persona formadora
            "teacher_has_knowledge",
            "teacher_resolved_doubts",
            "teacher_has_communication_skills",
            # Utilitat del curs
            "expectations_satisfied",
            "adquired_new_tools",
            "met_new_people",
            "wanted_start_cooperative",
            "wants_start_cooperative_now",
            # Valoració global
            "general_satisfaction",
            "also_interested_in",
            "heard_about_it",
            "comments",
        )
        TRUE_FALSE_CHOICES = ((True, "Yes"), (False, "No"))
        widgets = {
            "wants_start_cooperative_now": forms.Select(choices=TRUE_FALSE_CHOICES)
        }

    def get_grouped_fields(self, teacher=""):
        if teacher:
            teacher = f" ({teacher})"
        fieldsets = [
            (
                "Organització",
                {
                    "fields": [
                        {
                            "name": "duration",
                            "type": "stars",
                            "obj": self.fields.get("duration"),
                        },
                        {
                            "name": "hours",
                            "type": "stars",
                            "obj": self.fields.get("hours"),
                        },
                        {
                            "name": "information",
                            "type": "stars",
                            "obj": self.fields.get("information"),
                        },
                        {
                            "name": "on_schedule",
                            "type": "stars",
                            "obj": self.fields.get("on_schedule"),
                        },
                        {
                            "name": "included_resources",
                            "type": "stars",
                            "obj": self.fields.get("included_resources"),
                        },
                        {
                            "name": "space_adequation",
                            "type": "stars",
                            "obj": self.fields.get("space_adequation"),
                        },
                    ]
                },
            ),
            (
                "Continguts",
                {
                    "fields": [
                        {
                            "name": "contents",
                            "type": "stars",
                            "obj": self.fields.get("contents"),
                        },
                    ]
                },
            ),
            (
                "Metodologia",
                {
                    "fields": [
                        {
                            "name": "methodology_fulfilled_objectives",
                            "type": "stars",
                            "obj": self.fields.get("methodology_fulfilled_objectives"),
                        },
                        {
                            "name": "methodology_better_results",
                            "type": "stars",
                            "obj": self.fields.get("methodology_better_results"),
                        },
                        {
                            "name": "participation_system",
                            "type": "stars",
                            "obj": self.fields.get("participation_system"),
                        },
                    ]
                },
            ),
            (
                f"Valoració de la persona formadora{teacher}",
                {
                    "fields": [
                        {
                            "name": "teacher_has_knowledge",
                            "type": "stars",
                            "obj": self.fields.get("teacher_has_knowledge"),
                        },
                        {
                            "name": "teacher_resolved_doubts",
                            "type": "stars",
                            "obj": self.fields.get("teacher_resolved_doubts"),
                        },
                        {
                            "name": "teacher_has_communication_skills",
                            "type": "stars",
                            "obj": self.fields.get("teacher_has_communication_skills"),
                        },
                    ]
                },
            ),
            (
                "Utilitat del curs",
                {
                    "fields": [
                        {
                            "name": "expectations_satisfied",
                            "type": "stars",
                            "obj": self.fields.get("expectations_satisfied"),
                        },
                        {
                            "name": "adquired_new_tools",
                            "type": "stars",
                            "obj": self.fields.get("adquired_new_tools"),
                        },
                        {
                            "name": "met_new_people",
                            "type": "yesno",
                            "obj": self.fields.get("met_new_people"),
                        },
                        {
                            "name": "wanted_start_cooperative",
                            "type": "yesno",
                            "obj": self.fields.get("wanted_start_cooperative"),
                        },
                        {
                            "name": "wants_start_cooperative_now",
                            "type": "yesno",
                            "obj": self.fields.get("wants_start_cooperative_now"),
                        },
                    ]
                },
            ),
            (
                "Valoració global",
                {
                    "fields": [
                        {
                            "name": "general_satisfaction",
                            "type": "stars",
                            "obj": self.fields.get("general_satisfaction"),
                        },
                        {
                            "name": "also_interested_in",
                            "type": "text",
                            "obj": self.fields.get("also_interested_in"),
                        },
                        {
                            "name": "heard_about_it",
                            "type": "text",
                            "obj": self.fields.get("heard_about_it"),
                        },
                        {
                            "name": "comments",
                            "type": "text",
                            "obj": self.fields.get("comments"),
                        },
                    ]
                },
            ),
        ]
        return fieldsets


class EntityCreatedAdminForm(models.ModelForm):
    class Meta:
        model = CreatedEntity
        fields = (
            "project",
            "service",
            "sub_service",
            "subsidy_period",
            "circle",
            "entity",
        )

    def clean(self):
        super().clean()
        CreatedEntity.validate_extended_fields(
            self.cleaned_data.get("project"),
        )
        return self.cleaned_data
