from constance import config
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm as BasePasswordResetForm
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError
from django.urls import reverse

from apps.coopolis.mixins import FormDistrictValidationMixin
from apps.coopolis.widgets import XDSoftDatePickerInput
from conf.custom_mail_manager import MyMailTemplate


class LogInForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(), label="Mantenir la sessió oberta"
    )
    # referer = request.META.get('HTTP_REFERER')

    def clean(self):
        super().clean()
        if not self.cleaned_data.get("remember_me"):
            self.request.session.set_expiry(0)
        return self.cleaned_data


class MyAccountForm(FormDistrictValidationMixin, UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            "photo",
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
        )
        widgets = {
            "gender": forms.RadioSelect,
        }

    fieldsets = [
        (
            None,
            {"fields": ("photo",)},
        ),
        (
            None,
            {
                "fields": (
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
                )
            },
        ),
        (
            None,
            {
                "fields": (
                    "educational_level",
                    "discovered_us",
                    "employment_situation",
                    "project_involved",
                )
            },
        ),
    ]

    required_css_class = "required"
    first_name = forms.CharField(label="Nom", max_length=30)
    last_name = forms.CharField(label="Cognom", max_length=30, required=True)
    email = forms.EmailField(
        label="Correu electrònic",
        max_length=254,
        help_text="Requerit, ha de ser una adreça vàlida.",
    )
    birthdate = forms.DateField(
        label="Data de naixement", required=True, widget=XDSoftDatePickerInput()
    )
    # authorize_communications = forms.BooleanField(
    #     label="Accepto rebre informació sobre els serveis", required=False
    # )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        self.fields["id_number"].required = False
        self.label_suffix = ""
        if "password" in self.fields:
            self.fields.pop("password")

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
        if value and (
            model.objects.filter(id_number__iexact=value)
            .exclude(id=self.request.user.id)
            .exists()
        ):
            raise ValidationError("El DNI ja existeix.")
        return value


class PasswordResetForm(BasePasswordResetForm):
    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        mail = MyMailTemplate("EMAIL_PASSWORD_RESET")
        mail.to = to_email
        mail.subject_strings = {
            "ateneu_nom": config.PROJECT_FULL_NAME,
        }
        password_reset_url = settings.ABSOLUTE_URL + reverse(
            "password_reset_confirm",
            kwargs={
                "uidb64": context["uid"],
                "token": context["token"],
            },
        )
        mail.body_strings = {
            "persona_nom": context["user"].first_name,
            "persona_email": context["email"],
            "absolute_url": settings.ABSOLUTE_URL,
            "password_reset_url": password_reset_url,
            "url_web_ateneu": config.PROJECT_WEBSITE_URL,
        }
        mail.send()
