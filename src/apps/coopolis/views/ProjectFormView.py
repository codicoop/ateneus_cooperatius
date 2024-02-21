from constance import config
from django import urls
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic

from apps.coopolis.forms import (
    ProjectCharacteristicsForm,
    ProjectForm,
    ProjectStageAttachForm,
    ProjectStageInitialPetitionForm,
    ProjectStageStartForm,
)
from apps.coopolis.models import Project
from apps.coopolis.views import LoginSignupContainerView
from conf.custom_mail_manager import MyMailTemplate


class ProjectFormView(SuccessMessageMixin, generic.UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "project.html"
    success_message = "Dades del projecte actualitzades correctament."

    def get_success_url(self):
        return urls.reverse("edit_project")

    def get_object(self, queryset=None):
        return self.request.user.project

    def get(self, request):
        if self.request.user.project is None:
            return HttpResponseRedirect(urls.reverse("new_project"))
        return super().get(self, request)


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

        messages.success(
            self.request,
            "S'ha enviat una sol·licitud d'acompanyament del projecte. En els"
            " propers dies et contactarà una persona de l'ateneu per concertar"
            " una primera reunió.",
        )
        return HttpResponseRedirect(self.get_success_url())

    def get(self, request):
        if self.request.user.project is not None:
            return HttpResponseRedirect(urls.reverse("edit_project"))
        return super().get(self, request)


class ProjectInfoView(LoginSignupContainerView):
    template_name = "project_info.html"

    # def get(self, request, *args, **kwargs):
    #     if self.request.user.is_authenticated:
    #         if self.request.user.project:
    #             return HttpResponseRedirect(urls.reverse("edit_project"))
    #         else:
    #             return HttpResponseRedirect(urls.reverse("new_project"))
    #     return super().get(self, request, *args, **kwargs)


def project_stage_view(request):
    projects = Project.objects.filter(partners=request.user)
    return render(request, "project_.html", {"projects": projects})


def project_stage_start_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, "project_.html", {"project": project})


def project_stage_data_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectStageStartForm(request.POST, instance=project)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("project_stage_attatch", pk=pk)
    else:
        form = ProjectStageStartForm(instance=project)
    return render(request, "project_.html", {"form": form})


def project_stage_attatch_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectStageAttachForm(request.POST, instance=project)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("project_stage_initial_petition", pk=pk)
    else:
        form = ProjectStageAttachForm(instance=project)
    return render(request, "project_.html", {"form": form})


def project_stage_initial_petition_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectStageInitialPetitionForm(request.POST, instance=project)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("project_stage_characteristics", pk=pk)
    else:
        form = ProjectStageInitialPetitionForm(instance=project)
    return render(request, "project_.html", {"form": form})


def project_stage_characteristics_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectCharacteristicsForm(request.POST, instance=project)
    if request.method == "POST":
        if form.is_valid():
            newproject = form.save()
            newproject.notify_new_request_to_ateneu()
            newproject.notify_request_confirmation()
            return redirect("project_info")
    else:
        form = ProjectCharacteristicsForm(instance=project)
    return render(request, "project_.html", {"form": form})
