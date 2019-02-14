#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from coopolis.models import User
from simple_history.admin import SimpleHistoryAdmin


class UserInline(admin.StackedInline):
    model = User
    fields = ('first_name',)
    extra = 0


class ProjectAdmin(SimpleHistoryAdmin):
    # TODO: Pulir això.
    '''inlines = [
        UserInline,
    ]'''

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "project_responsible":
            kwargs["queryset"] = User.objects.filter(is_staff=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def _users(self, obj):
        return obj.projects.all().count()
