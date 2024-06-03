from django.contrib import admin
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse_lazy

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
from ..models.general import Customization

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
    search_fields = ("name", )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Customization)
class CustomizationAdmin(admin.ModelAdmin):
    list_display = (
        "logo",
        "signatures_pdf_footer",
    )
    fieldsets = (
        (
            "Imatges",
            {
                "fields": (
                    "logo",
                    "signatures_pdf_footer",
                )
            },
        ),
    )
    save_as_continue = False
    save_as = False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        if Customization.objects.all().count() > 0:
            return False
        return True

    def changelist_view(self, request, extra_context=None):
        objs = Customization.objects.all()
        if len(objs) < 1:
            return redirect(reverse_lazy("admin:coopolis_customization_add"))
        return redirect(
            reverse_lazy(
                "admin:coopolis_customization_change",
                kwargs={"object_id": objs[0].pk},
            )
        )

    def response_change(self, request, obj):
        """
        This controls the response after the change view is saved.
        """
        return redirect(reverse_lazy("admin:index"))
