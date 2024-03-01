from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.cc_courses.choices import ProjectStageStatesChoices
from apps.coopolis.forms import (
    ProjectCharacteristicsForm,
    ProjectStageAttachForm,
    ProjectStageInitialPetitionForm,
    ProjectStageStartForm,
)
from apps.coopolis.models import Project, ProjectStage, ProjectStageSession
from apps.dataexports.models import SubsidyPeriod


@login_required
def project_stage_view(request):
    projects = Project.objects.filter(partners=request.user)
    return render(request, "project_info.html", {"projects": projects})


@login_required
def project_stage_start_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project_stages = project.stages.filter(
        stage_state__in=[
            ProjectStageStatesChoices.OPEN,
            ProjectStageStatesChoices.PENDING,
        ]
    )
    if request.user not in project.partners.all() or project_stages:
        return redirect("home")
    return render(request, "project_stage_start.html", {"project": project})


@login_required
def project_stage_data_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project_stages = project.stages.filter(
        stage_state__in=[
            ProjectStageStatesChoices.OPEN,
            ProjectStageStatesChoices.PENDING,
        ]
    )
    if request.user not in project.partners.all() or project_stages:
        return redirect("home")
    if request.method == "POST":
        form = ProjectStageStartForm(request.POST, instance=project)
        if form.is_valid():
            project.is_draft = True
            project.save()
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
    project_stages = project.stages.filter(
        stage_state__in=[
            ProjectStageStatesChoices.OPEN,
            ProjectStageStatesChoices.PENDING,
        ]
    )
    if request.user not in project.partners.all() or project_stages:
        return redirect("home")
    if request.method == "POST":
        form = ProjectStageAttachForm(request.POST, request.FILES, instance=project)
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
    project_stages = project.stages.filter(
        stage_state__in=[
            ProjectStageStatesChoices.OPEN,
            ProjectStageStatesChoices.PENDING,
        ]
    )
    if request.user not in project.partners.all() or project_stages:
        return redirect("home")
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
    if request.user not in project.partners.all():
        return redirect("home")
    if request.method == "POST":
        form = ProjectCharacteristicsForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            project.is_draft = False
            project.save()
            # project.partners.add(request.user)
            new_project_stage = ProjectStage()
            new_project_stage.project = project
            new_project_stage.stage_state = ProjectStageStatesChoices.PENDING
            new_project_stage.subsidy_period = SubsidyPeriod.objects.latest(
                "date_start"
            )
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
    if request.user not in project.partners.all():
        return redirect("home")
    context = {}
    context["project"] = project
    pending_project_stages = ProjectStage.objects.filter(
        project=project, stage_state=ProjectStageStatesChoices.PENDING
    )
    open_project_stages = ProjectStage.objects.filter(
        project=project, stage_state=ProjectStageStatesChoices.OPEN
    )
    context["is_draft"] = project.is_draft
    context["is_pending"] = pending_project_stages
    context["is_open"] = open_project_stages
    if request.method == "POST" and "delete" in request.POST:
        project.is_draft = False
        project.object_finality = ""
        project.project_status = ""
        project.motivation = ""
        project.save()
        messages.success(
            request,
            "Dades del acompanyament borrades correctament.",
        )
        return redirect("project_stage_sessions", pk=pk)
    return render(request, "project_stage_sessions.html", context)
