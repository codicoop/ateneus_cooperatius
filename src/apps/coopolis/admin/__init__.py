from django.contrib import admin
from django.conf import settings

from apps.coopolis.models import (
    User, Project, ProjectStage, Derivation, EmploymentInsertion,
    ActivityPoll, StageSubtype, Town,
)
from .ProjectAdmin import (
    ProjectAdmin, ProjectStageAdmin, DerivationAdmin, EmploymentInsertionAdmin,
    StageSubtypeAdmin, ProjectFile, ProjectFileAdmin,
)
# We're not registering it here, but needed the import so grappelli's
# dashboard can work.
from .ProjectsFollowUpAdmin import ProjectsConstitutedServiceAdmin
from .UserAdmin import UserAdmin
from .ActivityPollAdmin import ActivityPollAdmin


admin.site.register(User, UserAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectStage, ProjectStageAdmin)
admin.site.register(Derivation, DerivationAdmin)
admin.site.register(EmploymentInsertion, EmploymentInsertionAdmin)
admin.site.register(ActivityPoll, ActivityPollAdmin)
admin.site.register(StageSubtype, StageSubtypeAdmin)
admin.site.register(ProjectFile, ProjectFileAdmin)

admin.site.site_header = settings.ADMIN_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.index_title = settings.ADMIN_INDEX_TITLE


@admin.register(Town)
class TownAdmin(admin.ModelAdmin):
    search_fields = ("name", "name_for_justification", )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
