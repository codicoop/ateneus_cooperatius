#!/usr/bin/env python
# -*- coding: utf-8 -*-

from simple_history.admin import SimpleHistoryAdmin


class UserAdmin(SimpleHistoryAdmin):
    list_display = ('id_number', 'last_name', 'first_name', 'email', 'project')
    search_fields = ('id_number', 'last_name', 'first_name', 'email', 'phone_number', 'cooperativism_knowledge')
    list_filter = ('gender', 'project', 'residence_town', 'residence_district', 'is_staff')
    fields = ['first_name', 'last_name', 'surname2', 'id_number', 'email', 'birthdate', 'birth_place',
              'residence_town', 'residence_district', 'address', 'phone_number', 'educational_level',
              'employment_situation', 'discovered_us', 'cooperativism_knowledge', 'project', 'is_staff', 'groups',
              'is_active', 'date_joined', 'last_login']
    readonly_fields = ('last_login', 'date_joined')

    def get_fields(self, request, obj=None):
        if request.user.is_superuser and "is_superuser" not in self.fields:
            self.fields.append('is_superuser')
        return super().get_fields(self, request)
