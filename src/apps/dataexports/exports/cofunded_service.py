from apps.cc_courses.models import Activity
from django.conf import settings

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
            cofunded__isnull=False
        )
        return obj
