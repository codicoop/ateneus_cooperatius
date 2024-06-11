from django import urls
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.views import generic

from apps.cc_courses.choices import ProjectStageStatesChoices
from apps.coopolis.forms import ProjectForm
from apps.coopolis.models import Project, ProjectStage, User
from apps.coopolis.views import LoginSignupContainerView


class ProjectFormView(SuccessMessageMixin, generic.UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "project_info.html"
    success_message = "Dades del projecte actualitzades correctament."

    def get_success_url(self):
        return urls.reverse("edit_project")

    def get_object(self, queryset=None):
        return self.request.user.project

    def get(self, request):
        if self.request.user.project is None:
            return HttpResponseRedirect(urls.reverse("new_project"))
        return super().get(self, request)

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
                "Dades del acompanyament borrades correctament.",
            )
            return HttpResponseRedirect(urls.reverse("edit_project"))
        if "add_partner" in request.POST:
            try:
                user = User.objects.filter(email=request.POST.get("email")).first()
                project = Project.objects.get(pk=request.POST.get("add_partner"))
                current_partners = project.partners.all()
                current_partners_list = set()
                for partner in current_partners:
                    current_partners_list.add(partner.pk)
                current_partners_list.add(user.id)
                project.partners.set(sorted(current_partners_list))
                project.save()
                messages.success(
                    request,
                    f"Invitació realitzada amb èxit a {user.full_name}."
                    "Se li ha enviat a l'usuari un correu per a la seva acceptació.",
                )
            except:
                messages.error(
                    request,
                    "L'usuari no existeix.",
                )
        if "delete_partner" in request.POST:
            user = User.objects.filter(id=request.POST.get("partner_id")).first()
            project = Project.objects.get(pk=request.POST.get("delete_partner"))
            current_partners = project.partners.all().exclude(id=user.id)
            current_partners_list = set()
            for partner in current_partners:
                current_partners_list.add(partner.pk)
            project.partners.set(sorted(current_partners_list))
            project.save()
            messages.success(
                request,
                f"{user.full_name} ha estat eliminada amb èxit d'aquest projecte.",
            )

        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.request.user.project
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
        return context


class ProjectCreateFormView(SuccessMessageMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "project.html"
    extra_context = {"show_new_project_info": True}

    def get_success_url(self):
        return urls.reverse("edit_project")

    def form_valid(self, form):
        newproject = form.save()
        newproject.partners.add(self.request.user)
        messages.success(self.request, "Dades del projecte guardades correctament.")
        return HttpResponseRedirect(self.get_success_url())

    def get(self, request):
        if self.request.user.project is not None:
            return HttpResponseRedirect(urls.reverse("edit_project"))
        return super().get(self, request)


class ProjectInfoView(LoginSignupContainerView):
    template_name = "project_empty.html"

    # def get(self, request, *args, **kwargs):
    #     if self.request.user.is_authenticated:
    #         if self.request.user.project:
    #             return HttpResponseRedirect(urls.reverse("edit_project"))
    #         else:
    #             return HttpResponseRedirect(urls.reverse("new_project"))
    #     return super().get(self, request, *args, **kwargs)
