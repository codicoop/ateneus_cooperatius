#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from coopolis.models import User, Project
from django.utils.safestring import mark_safe
from coopolis.mixins import ExportCsvMixin


class ProjectAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('name', 'web', 'mail', 'phone', 'project_responsible', 'registration_date', 'subsidy_period',
                    'partners_field')
    search_fields = ('name', 'web', 'mail', 'phone', 'registration_date', 'object_finality', 'project_origins',
                     'solves_necessities', 'social_base', 'sector')
    list_filter = (('project_responsible', admin.RelatedOnlyFieldListFilter), 'registration_date', 'subsidy_period',
                   'sector')
    actions = ["export_as_csv"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "project_responsible":
            kwargs["queryset"] = User.objects.filter(is_staff=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def _users(self, obj):
        return obj.projects.all().count()

    def partners_field(self, obj):
        return mark_safe(u'<a href="../../%s/%s?project__exact=%d">Sòcies</a>' % (
            'coopolis', 'user', obj.id))

    partners_field.short_description = 'Llistat'
