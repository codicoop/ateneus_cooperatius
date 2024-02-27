from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.coopolis.forms import (
    ProjectCharacteristicsForm,
    ProjectStageAttachForm,
    ProjectStageInitialPetitionForm,
    ProjectStageStartForm,
)
from apps.coopolis.models import Project, ProjectStage, ProjectStageSession


@login_required
def project_stage_view(request):
    projects = Project.objects.filter(partners=request.user)
    return render(request, "project_info.html", {"projects": projects})


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
    if request.method == "POST":
        form = ProjectCharacteristicsForm(request.POST, instance=project)
        if form.is_valid():
            new_project = form.save()
            new_project.partners.add(request.user)
            new_project_stage = ProjectStage()
            new_project_stage.project = new_project
            new_project_stage.save()
            project.notify_new_request_to_ateneu()
            project.notify_request_confirmation()
            
            messages.success(
                request,
                "S'ha enviat una sol·licitud d'acompanyament del projecte. En els"
                " propers dies et contactarà una persona de l'ateneu per concertar"
                " una primera reunió.",
            )
            return redirect("project_stage_characteristics", pk=pk)
    else:
        form = ProjectCharacteristicsForm(instance=project)
    return render(
        request,
        "project_stage_characteristics.html",
        {
            "project": project,
            "form": form,
        },
    )


@login_required
def project_stage_sessions_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    context = {
        "project": project,
    }
    return render(request, "project_stage_sessions.html", context)
