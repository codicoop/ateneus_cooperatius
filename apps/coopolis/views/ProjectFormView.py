#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django import urls
from django.http import HttpResponseRedirect
from coopolis.models import Project, ProjectStage
from coopolis.forms import ProjectForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from coopolis.views import LoginSignupContainerView
from constance import config


class ProjectFormView(SuccessMessageMixin, generic.UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project.html'
    success_message = "Dades del projecte actualitzades correctament."

    def get_success_url(self):
        return urls.reverse('edit_project')

    def get_object(self, queryset=None):
        return self.request.user.project

    def get(self, request):
        if self.request.user.project is None:
            return HttpResponseRedirect(urls.reverse('new_project'))
        return super().get(self, request)


class ProjectCreateFormView(SuccessMessageMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project.html'
    extra_context = {'show_new_project_info': True}

    def get_success_url(self):
        return urls.reverse('edit_project')

    def form_valid(self, form):
        newproject = form.save()
        newstage = ProjectStage(project=newproject)
        newstage.save()
        newstage.involved_partners.add(self.request.user)
        mail_to = {config.EMAIL_TO_DEBUG}
        if settings.DEBUG is not True:
            mail_to.add(config.EMAIL_TO)
        message = config.EMAIL_NEW_PROJECT.format(
                        newproject.name,
                        newproject.phone,
                        newproject.mail,
                        self.request.user.email
            )
        send_mail(
            subject=config.EMAIL_NEW_PROJECT_SUBJECT.format(newproject.name),
            message=message,
            html_message=message,
            recipient_list=mail_to,
            from_email=settings.DEFAULT_FROM_EMAIL
        )
        messages.success(self.request, "S'ha enviat una sol·licitud d'acompanyament del projecte. En els propers dies "
                                       "et contactarà una persona de Coòpolis per concertar una primera reunió.")
        return HttpResponseRedirect(self.get_success_url())

    def get(self, request):
        if self.request.user.project is not None:
            return HttpResponseRedirect(urls.reverse('edit_project'))
        return super().get(self, request)


class ProjectInfoView(LoginSignupContainerView):
    template_name = "project_info.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.project:
                return HttpResponseRedirect(urls.reverse('edit_project'))
            else:
                return HttpResponseRedirect(urls.reverse('new_project'))
        return super().get(self, request, *args, **kwargs)
