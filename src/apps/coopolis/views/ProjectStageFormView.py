from constance import config
from django import urls
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from apps.coopolis.forms import (
    ProjectCharacteristicsForm,
    ProjectStageAttachForm,
    ProjectStageInitialPetitionForm,
    ProjectStageStartForm,
)
from apps.coopolis.models import Project
from apps.coopolis.views import LoginSignupContainerView
from conf.custom_mail_manager import MyMailTemplate


@login_required
def project_stage_view(request):
    projects = Project.objects.filter(partners=request.user)
    return render(request, "project_.html", {"projects": projects})


@login_required
def project_stage_start_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, "project_stage_start.html", {"project": project})


@login_required
def project_stage_data_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectStageStartForm(request.POST, instance=project)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("project_stage_attatch", pk=pk)
    else:
        form = ProjectStageStartForm(instance=project)
    return render(
        request, "project_stage_data.html", {"project": project, "form": form}
    )


@login_required
def project_stage_attatch_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectStageAttachForm(request.POST, instance=project)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("project_stage_initial_petition", pk=pk)
    else:
        form = ProjectStageAttachForm(instance=project)
    return render(
        request, "project_stage_attatch.html", {"project": project, "form": form}
    )


@login_required
def project_stage_initial_petition_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectStageInitialPetitionForm(request.POST, instance=project)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("project_stage_characteristics", pk=pk)
    else:
        form = ProjectStageInitialPetitionForm(instance=project)
    return render(
        request,
        "project_stage_initial_petition.html",
        {"project": project, "form": form},
    )


@login_required
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
    return render(
        request,
        "project_stage_characteristics.html",
        {"project": project, "form": form},
    )


@login_required
def project_stage_sessions_view(request, pk):
    project = get_object_or_404(Project, pk=pk)

    return render(
        request,
        "project_stage_sessions.html",
        {
            "project": project,
        },
    )
