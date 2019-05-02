#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.conf import settings
from coopolis.models import User, Project, ProjectStage, ProjectStageType
from cc_courses.models import Course, Activity, CoursePlace, Entity, Organizer
from .ActivityAdmin import ActivityAdmin
from .CourseAdmin import CourseAdmin
from .ProjectAdmin import ProjectAdmin, ProjectStageAdmin
from .UserAdmin import UserAdmin
from .CoursePlaceAdmin import CoursePlaceAdmin


admin.site.register(User, UserAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectStage, ProjectStageAdmin)
admin.site.register(ProjectStageType)
admin.site.register(Course, CourseAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(CoursePlace, CoursePlaceAdmin)
admin.site.register(Entity)
admin.site.register(Organizer)

admin.site.site_header = settings.ADMIN_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.index_title = settings.ADMIN_INDEX_TITLE
