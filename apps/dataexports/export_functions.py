from django.http import HttpResponseNotFound

from dataexports.exports.cofunded import ExportJustificationCofunded
from dataexports.exports.justification import ExportJustification
from dataexports.exports.justification_2_itineraris import (
    ExportJustification2Itineraris
)
from dataexports.exports.memory import ExportMemory
from dataexports.models import DataExports


class ExportFunctions:
    """
    This is the generation of excel-like data (in .xlsx) made to fit
    the official formats required for the justification of the
    subsidies.

    Given that each year it changes, and we might need multiple
    documents, or even each Ateneu might need a specific document
    for subsidies that are not the 'conveni', we created a simple
    system to create different functions, 'register' them in the
    admin, and launch them from there.

    This class holds the functions that generate this .xlsx.

    To use them, call callmethod('function_name')
    """
    def callmethod(self, name):
        if hasattr(self, name):
            obj = DataExports.objects.get(function_name=name)
            return getattr(self, name)(obj)
        else:
            message = "<h1>La funció especificada no existeix</h1>"
            return HttpResponseNotFound(message)

    def export_stages_descriptions(self, export_obj):
        controller = ExportMemory()
        return controller.export_stages_descriptions(export_obj)

    def export(self, export_obj):
        controller = ExportJustification()
        return controller.export(export_obj)

    def export_dos_itineraris(self, export_obj):
        controller = ExportJustification2Itineraris()
        return controller.export_dos_itineraris(export_obj)

    def export_cofunded(self, export_obj):
        controller = ExportJustificationCofunded()
        return controller.export(export_obj)
