from dataexports.exports.justification import ExportJustification


class ExportJustification2Itineraris(ExportJustification):
    """

    Exportació justificació en 2 itineraris

    """

    def export_dos_itineraris(self, export_obj):
        self.export_manager.stages_groups = {
            1: 'nova_creacio',
            2: 'nova_creacio',
            6: 'nova_creacio',
            7: 'consolidacio',
            8: 'consolidacio',
            9: 'incubacio'
        }
        return self.export(export_obj)
