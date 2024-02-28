from constance import config
from django import urls
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.views import generic

from apps.cc_courses.choices import ProjectStageStatesChoices
from apps.coopolis.forms import ProjectForm
from apps.coopolis.models import Project, ProjectStage
from apps.coopolis.views import LoginSignupContainerView
from conf.custom_mail_manager import MyMailTemplate


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
