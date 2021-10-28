from coopolis.models import ActivityPoll
from dataexports.exports.manager import ExcelExportManager


class GlobalReportRow:
    def __init__(
            self,
            title,
            ateneu=0,
            cercle1=0,
            cercle2=0,
            cercle3=0,
            cercle4=0
    ):
        self.title = title
        self.ateneu = ateneu
        self.cercle1 = cercle1
        self.cercle2 = cercle2
        self.cercle3 = cercle3
        self.cercle4 = cercle4


class ExportPolls:
    def __init__(self, export_obj):
        self.export_manager = ExcelExportManager(export_obj)

    def export(self):
        """ Each function here called handles the creation of one of the
        worksheets."""
        self.export_polls()

        return self.export_manager.return_document("hores_covid")

    def export_polls(self):
        self.export_manager.worksheet.title = "Acompanyaments covid"
        self.export_manager.row_number = 1

        columns = [
            ("", 60),
            ("Ateneu Cooperatiu", 20),
            ("Cercle 1", 20),
            ("Cercle 2", 20),
            ("Cercle 3", 20),
            ("Cercle 4", 20),
        ]
        self.export_manager.create_columns(columns)

        self.polls_rows()

    def global_report_obj(self):
        return ActivityPoll.objects.filter(
            created__range=self.export_manager.subsidy_period_range,
        )

    def polls_rows(self):
        rows = [
            GlobalReportRow("Nombre d'enquestes de satisfacció valorades"),
            GlobalReportRow("Valoracions globals"),
            GlobalReportRow("Valoració global de les actuacions"),
            GlobalReportRow("Organització"),
            GlobalReportRow("La durada ha estat l'adequada?"),
            GlobalReportRow("Els horaris han estat adequats?"),
            GlobalReportRow("Informació necessària per fer l'activitat"),
            GlobalReportRow("S'han complert les dates, horaris, etc..."),
            GlobalReportRow("Els espais han estat adequats (sales, aules, plataforma digital...)"),
            GlobalReportRow("Continguts"),
            GlobalReportRow("Els continguts han estat adequats"),
            GlobalReportRow("Metodologia"),
            GlobalReportRow("La metodologia ha estat coherent amb els objectius"),
            GlobalReportRow("La metodologia ha permès obtenir millors resultats"),
            GlobalReportRow("El sistema de participació i resolució de dubtes ha estat adequat?"),
            GlobalReportRow("Valoració de la persona formadora"),
            GlobalReportRow("Ha mostrat coneixements i experiència sobre el tema?"),
            GlobalReportRow("Ha aconseguit resoldre els problemes i dubtes que s’ha plantejat?"),
            GlobalReportRow("El professional ha mostrat competències comunicatives?"),
            GlobalReportRow("Utilitat del curs"),
            GlobalReportRow("Ha satisfet les meves expectatives"),
            GlobalReportRow("He incorporat eines per aplicar a nous projectes"),
            GlobalReportRow("M'ha permès conèixer persones afins"),
            GlobalReportRow("Abans del curs, teníeu ganes/necessitats d'engegar algun projecte cooperatiu"),
            GlobalReportRow("I després?"),
            GlobalReportRow("Valoració global"),
            GlobalReportRow("Grau de satisfacció general"),
        ]
        # polls_obj = self.global_report_obj()

        for row in rows:
            self.export_manager.row_number += 1
            self.export_manager.fill_row_data(
                [
                    row.title,
                    row.ateneu,
                    row.cercle1,
                    row.cercle2,
                    row.cercle3,
                    row.cercle4,
                ]
            )
