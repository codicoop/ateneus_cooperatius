#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from coopolis.models import User, ProjectStage
from django.utils.safestring import mark_safe
from coopolis.mixins import ExportCsvMixin


class ProjectAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('name', 'web', 'mail', 'phone', 'registration_date', 'stages_field')
    search_fields = ('name', 'web', 'mail', 'phone', 'registration_date', 'object_finality', 'project_origins',
                     'solves_necessities', 'social_base', 'sector')
    list_filter = ('registration_date', 'sector')
    actions = ["export_as_csv"]

    def stages_field(self, obj):
        return mark_safe(u'<a href="../../%s/%s?project__exact=%d">Veure</a>' % (
            'coopolis', 'projectstage', obj.id))

    stages_field.short_description = 'Fases'


class ProjectStageAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('project', 'date_start', 'stage_responsible', 'stage', 'axis', 'organizer', 'subsidy_period',
                    'project_field')
    list_filter = ('subsidy_period', ('stage_responsible', admin.RelatedOnlyFieldListFilter), 'date_start',
                   'axis', 'organizer', 'project__sector')
    actions = ["export_as_csv"]
    search_fields = ['project__name']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "stage_responsible":
            kwargs["queryset"] = User.objects.filter(is_staff=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def project_field(self, obj):
        return mark_safe(u'<a href="../../%s/%s/%d/change">%s</a>' % (
            'coopolis', 'project', obj.project.id, 'Veure'))

    project_field.short_description = 'Fitxa'

    # define the raw_id_fields
    raw_id_fields = ('involved_partners',)
    # define the autocomplete_lookup_fields
    autocomplete_lookup_fields = {
        'm2m': ['involved_partners'],
    }
