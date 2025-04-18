from itertools import islice

from django import urls
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordChangeView as BasePasswordChangeView
from django.contrib.auth.views import (
    PasswordResetCompleteView as BasePasswordResetCompleteView,
)
from django.contrib.auth.views import (
    PasswordResetConfirmView as BasePasswordResetConfirmView,
)
from django.contrib.auth.views import PasswordResetDoneView as BasePasswordResetDoneView
from django.contrib.auth.views import PasswordResetView as BasePasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from apps.cc_users.forms import MyAccountForm, PasswordResetForm
from apps.coopolis.models import User

from .decorators import anonymous_required


class UsersLoginView(LoginView):
    redirect_authenticated_user = True

    def get_success_url(self):
        return super().resolve_url(self.request.get_redirect_url())


class MyAccountView(SuccessMessageMixin, UpdateView):
    template_name = "registration/profile.html"
    form_class = MyAccountForm
    model = User
    success_message = "Dades modificades correctament"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return urls.reverse("user_profile")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def post(self, request, *args, **kwargs):
        if "delete" in request.POST:
            user = self.get_object()
            user.is_active = False
            user.save()
            return redirect("home")
        return super().post(request, *args, **kwargs)


class PasswordResetView(BasePasswordResetView):
    form_class = PasswordResetForm

    @method_decorator(anonymous_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        user = form.get_users(form.cleaned_data["email"])
        # get_users is a generator, but our email field is unique.
        # This is the simplest way to retrieve only 1 item from a generator:
        user_list = list(islice(user, 1))
        if len(user_list) == 0 or not user_list[0].is_active:
            error = ValidationError(
                {
                    "email": "El correu indicat no correspon a cap compte "
                    "registrat, si us plau verifica que l'hagis "
                    "escrit correctament."
                },
                code="inexistent_email",
            )
            form.add_error(None, error)
            return super().form_invalid(form)
        return super().form_valid(form)


class PasswordResetConfirmView(BasePasswordResetConfirmView):
    @method_decorator(anonymous_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class PasswordResetDoneView(BasePasswordResetDoneView):
    @method_decorator(anonymous_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class PasswordResetCompleteView(BasePasswordResetCompleteView):
    @method_decorator(anonymous_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class PasswordChangeView(BasePasswordChangeView):
    template_name = "registration/password.html"
