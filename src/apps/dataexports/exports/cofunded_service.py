from apps.cc_courses.models import Activity
from apps.coopolis.models import ProjectStage

from apps.dataexports.exports.justification_service import \
    ExportJustificationService


class ExportJustificationCofundedService(ExportJustificationService):
    """
    
    Exportació cofinançades per Servei / Subservei
    
    """
    def export(self):
        # Each function called here handles the creation of each worksheets
        self.export_actuacions()
        self.export_participants()

        return self.export_manager.return_document("cofinançades")

    def get_sessions_obj(self, for_minors=False):
        obj = Activity.objects.filter(
            date_start__range=self.export_manager.subsidy_period.range,
            cofunded__isnull=False,
            for_minors=for_minors,
            exclude_from_justification=False
        )
        return obj

    def get_stages_obj(self):
        return ProjectStage.objects.order_by('date_start').filter(
            subsidy_period=self.export_manager.subsidy_period,
            cofunded__isnull=False,
            exclude_from_justification=False,
        )
