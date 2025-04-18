from constance import config

from apps.coopolis.helpers import absolute_url
from apps.coopolis.models.invitation import Invitation
from conf import settings
from django import urls
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.views import generic
from django.shortcuts import get_object_or_404
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

from apps.cc_courses.choices import ProjectStageStatesChoices
from apps.coopolis.forms import ProjectForm
from apps.coopolis.models import Project, ProjectStage, User
from apps.coopolis.models.invitation import Invitation
from apps.coopolis.views import LoginSignupContainerView
from conf.post_office import send


class ProjectFormView(SuccessMessageMixin, generic.UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "project_info.html"
    success_message = "Dades del projecte actualitzades correctament."

    def get_success_url(self):
        return urls.reverse("edit_project", kwargs={"pk": self.object.pk})

    def get_object(self, queryset=None):
        return get_object_or_404(
            Project, pk=self.kwargs["pk"], partners__id=self.request.user.id
        )

    def post(self, request, *args, **kwargs):
        if "delete" in request.POST:
            project = Project.objects.get(pk=request.POST.get("delete"))
            project.is_draft = False
            project.object_finality = ""
            project.project_status = ""
            project.motivation = ""
            project.save()
            messages.success(
                request,
                "Dades de l'acompanyament esborrades correctament.",
            )
            return HttpResponseRedirect(
                urls.reverse("edit_project", kwargs={"pk": project.pk})
            )
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_id = self.kwargs.get("pk")
        project = Project.objects.get(pk=object_id)
        pending_project_stages = ProjectStage.objects.filter(
            project=project, stage_state=ProjectStageStatesChoices.PENDING
        )
        open_project_stages = ProjectStage.objects.filter(
            project=project, stage_state=ProjectStageStatesChoices.OPEN
        )
        context["is_draft"] = project.is_draft
        context["is_pending"] = pending_project_stages
        context["is_open"] = open_project_stages
        context["partners"] = User.objects.filter(projects=project.id)
        invited_users = Invitation.objects.filter(project=project).values("user")
        users = set()
        if invited_users:
            for user in invited_users:
                users.add(User.objects.filter(id=user["user"]).first())
        context["invited_partners"] = users
        return context


@login_required
def project_partner_manage(request):
    project_pk = None
    if request.method == "POST":
        if "add_partner" in request.POST:
            project_pk = request.POST.get("add_partner")
            project = Project.objects.get(pk=project_pk)
            validator = EmailValidator()
            try:
                validator(request.POST.get("email"))
            except ValidationError:
                messages.error(
                    request,
                    "Ha d'indicar un correu electrònic vàlid.",
                )
                return redirect("edit_project", pk=project_pk)
            try:
                user = User.objects.get(email=request.POST.get("email"))
            except User.DoesNotExist:
                messages.error(
                    request,
                    "L'usuari no existeix.",
                )
                return redirect("edit_project", pk=project_pk)
            user_is_invited = (
                Invitation.objects.filter(user=user, project=project)
                .values("user__id")
                .first()
            )
            if user_is_invited:
                messages.error(
                    request,
                    f"L'usuari {user.full_name} ja està convidat.",
                )
                return redirect("edit_project", pk=project_pk)
            user_is_partner = project.partners.filter(id=user.id).first()
            if user_is_partner:
                messages.error(
                    request,
                    f"L'usuari {user.full_name} ja forma part d'aquest projecte.",
                )
                return redirect("edit_project", pk=project_pk)
            invitation = Invitation.objects.create(user=user, project=project)
            context = {
                "persona_fullname": user.full_name,
                "persona_email": user.email,
                "project": project.name,
                "absolute_url": settings.ABSOLUTE_URL,
                "invitation_url": absolute_url(
                    urls.reverse(
                        "invitation_project",
                        kwargs={"uuid": invitation.uuid},
                    ),
                ),
            }
            send(
                recipients=user.email,
                context=context,
                template="EMAIL_PROJECT_INVITATION",
            )
            messages.success(
                request,
                f"Invitació realitzada amb èxit a {user.full_name}."
                " Se li ha enviat un correu per a la seva acceptació.",
            )
        if "delete_partner" in request.POST:
            project_pk = request.POST.get("delete_partner")
            try:
                project = Project.objects.get(pk=project_pk)
            except Project.DoesNotExist:
                messages.error(
                    request,
                    "Aquest projecte no existeix.",
                )
                return redirect("home")
            try:
                user = User.objects.get(id=request.POST.get("partner_id"))
            except User.DoesNotExist:
                messages.error(
                    request,
                    "Aquest usuari no existeix.",
                )
                return redirect("edit_project", pk=project.pk)
            if user == request.user:
                messages.error(
                    request,
                    "No et pots eliminar a tu mateix/a del projecte.",
                )
                return redirect("edit_project", pk=project.pk)
            try:
                project = Project.objects.get(pk=request.POST.get("delete_partner"))
            except Project.DoesNotExist:
                messages.error(
                    request,
                    "Aquest projecte no existeix.",
                )
                return redirect("edit_project", pk=project.pk)
            project.partners.remove(user)

            context = {
                "persona_fullname": user.full_name,
                "persona_email": user.email,
                "project": project.name,
            }
            send(
                recipients=config.EMAIL_FROM_PROJECTS.split(","),
                template="EMAIL_PARTNER_ELIMINATION",
                context=context,
            )
            messages.success(
                request,
                f"{user.full_name} ha estat eliminada amb èxit d'aquest projecte.",
            )
        if "delete_invitation" in request.POST:
            project_pk = request.POST.get("delete_invitation")
            try:
                user = User.objects.get(id=request.POST.get("invited_id"))
            except User.DoesNotExist:
                messages.error(
                    request,
                    "Aquest usuari no existeix.",
                )
                return redirect("edit_project", pk=project_pk)
            try:
                invitation = Invitation.objects.get(
                    user=user, project=request.POST.get("delete_invitation")
                )
            except Invitation.DoesNotExist:
                messages.error(
                    request,
                    "Aquesta invitació no existeix.",
                )
                return redirect("edit_project", pk=project_pk)
            invitation.delete()
            messages.success(
                request,
                f"{user.full_name} ha estat eliminada amb èxit d'aquest projecte.",
            )
    return redirect("edit_project", pk=project_pk)


@login_required
def invitation_partner(request, uuid):
    if request.method == "GET":
        try:
            invitation = Invitation.objects.get(uuid=uuid)
        except Invitation.DoesNotExist:
            messages.error(
                request,
                "Aquest enllaç d'invitació no existeix.",
            )
            return redirect("home")
        if request.user.id != invitation.user.id:
            messages.error(
                request,
                "Estàs accedint a un enllaç d'invitació a un projecte que correspon a un altre usuari. "
                "Assegura't d'obrir l'enllaç des del compte a la qual t'han enviat la invitació.",
            )
            return redirect("home")
        context = {"project": invitation.project, "user": invitation.user}
        return render(request, "project_invitation.html", context=context)
    if request.method == "POST":
        project_pk = request.POST.get("project")
        try:
            invitation = Invitation.objects.get(uuid=uuid)
        except Invitation.DoesNotExist:
            messages.error(
                request,
                "Aquest enllaç d'invitació no existeix.",
            )
            return redirect("home")
        try:
            user = User.objects.get(id=invitation.user.id)
        except User.DoesNotExist:
            messages.error(
                request,
                "Aquest usuari no existeix.",
            )
            return redirect("home")
        if "accept" in request.POST:
            try:
                project = Project.objects.get(pk=project_pk)
            except Project.DoesNotExist:
                messages.error(
                    request,
                    "Aquest projecte no existeix.",
                )
                return redirect("home")
            project.partners.add(user)
            invitation.delete()
            messages.error(
                request,
                "Has acceptat formar part del projecte.",
            )
            return redirect("edit_project", pk=project_pk)
        if "deny" in request.POST:
            invitation.delete()
            messages.error(
                request,
                "Has rebutjat formar part del projecte.",
            )
            return redirect("home")
    return redirect("home")


class ProjectCreateFormView(SuccessMessageMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "project.html"
    extra_context = {"show_new_project_info": True}

    def get_success_url(self):
        return urls.reverse("edit_project", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        newproject = form.save()
        newproject.partners.add(self.request.user)
        messages.success(self.request, "Dades del projecte guardades correctament.")
        self.object = newproject
        return HttpResponseRedirect(self.get_success_url())


class ProjectInfoView(LoginSignupContainerView):
    template_name = "project_empty.html"

    # def get(self, request, *args, **kwargs):
    #     if self.request.user.is_authenticated:
    #         if self.request.user.project:
    #             return HttpResponseRedirect(urls.reverse("edit_project"))
    #         else:
    #             return HttpResponseRedirect(urls.reverse("new_project"))
    #     return super().get(self, request, *args, **kwargs)
