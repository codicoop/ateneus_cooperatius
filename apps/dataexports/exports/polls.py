from pprint import pprint

from django.db.models import Count, Avg, F, IntegerField

from cc_courses.models import Organizer
from coopolis.models import ActivityPoll
from dataexports.exports.manager import ExcelExportManager


class BaseRow:
    def get_columns(self) -> list:
        return []


class GlobalReportRow(BaseRow):
    def __init__(
            self,
            title: str,
            ateneu: int = 0,
            cercle1: int = 0,
            cercle2: int = 0,
            cercle3: int = 0,
            cercle4: int = 0,
            values_dict: dict = None,
            values_dict_field: str = None,
    ):
        self.title = title
        self.ateneu = ateneu
        self.cercle1 = cercle1
        self.cercle2 = cercle2
        self.cercle3 = cercle3
        self.cercle4 = cercle4
        if values_dict and values_dict_field:
            print(values_dict["cercle1"])
            self.ateneu = values_dict["ateneu"].get(values_dict_field)
            self.cercle1 = values_dict["cercle1"].get(values_dict_field)
            self.cercle2 = values_dict["cercle2"].get(values_dict_field)
            self.cercle3 = values_dict["cercle3"].get(values_dict_field)
            self.cercle4 = values_dict["cercle4"].get(values_dict_field)

    def get_columns(self) -> list:
        return [
            self.title,
            round(self.ateneu, 1),
            round(self.cercle1, 1),
            round(self.cercle2, 1),
            round(self.cercle3, 1),
            round(self.cercle4, 1),
        ]


class EmptyRow(BaseRow):
    pass


class TitleRow(BaseRow):
    def __init__(self, title: str):
        self.title = title

    def get_columns(self) -> list:
        return [self.title, ]


class ExportPolls:
    def __init__(self, export_obj):
        self.export_manager = ExcelExportManager(export_obj)
        self.organizers = dict()
        self.import_organizers()

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
            (self.organizers.get(0), 20),
            (self.organizers.get(1), 20),
            (self.organizers.get(2), 20),
            (self.organizers.get(3), 20),
            (self.organizers.get(4), 20),
        ]
        self.export_manager.create_columns(columns)

        self.polls_rows()

    def global_report_obj(self):
        querysets = []
        for organizer in self.organizers.values():
            pprint(self.export_manager.subsidy_period_range)
            querysets.append(
                ActivityPoll.objects.filter(
                    created__range=self.export_manager.subsidy_period_range,
                    activity__organizer=organizer,
                )
            )
        # qs.annotate(Count("id"))
        # qs.order_by()
        return querysets

    def get_averages_qs(self, queryset):
        return queryset.aggregate(
            Avg("duration"),
            Avg("hours"),
            Avg("information"),
            Avg("on_schedule"),
            Avg("included_resources"),
            Avg("space_adequation"),
            Avg("contents"),
            Avg("methodology_fulfilled_objectives"),
            Avg("methodology_better_results"),
            Avg("participation_system"),
        )

    def polls_rows(self):
        querysets = self.global_report_obj()
        total_organizers = len(querysets)
        if not total_organizers:
            return
        averages = {
            "ateneu": self.get_averages_qs(querysets[0]),
            "cercle1": {},
            "cercle2": {},
            "cercle3": {},
            "cercle4": {},
        }
        if total_organizers > 1:
            averages["cercle1"] = self.get_averages_qs(querysets[1])
        if total_organizers > 2:
            averages["cercle2"] = self.get_averages_qs(querysets[2])
        if total_organizers > 3:
            averages["cercle3"] = self.get_averages_qs(querysets[3])
        if total_organizers > 4:
            averages["cercle4"] = self.get_averages_qs(querysets[4])
        print("cercle4 després d'assignar-lo:", averages["cercle4"])

        # pprint(averages)
        rows = [
            GlobalReportRow(
                "Nombre d'enquestes de satisfacció valorades",
                querysets[0].count(),
                querysets[1].count() if total_organizers > 1 else "-",
                querysets[2].count() if total_organizers > 2 else "-",
                querysets[3].count() if total_organizers > 3 else "-",
                querysets[4].count() if total_organizers > 4 else "-",
            ),
            EmptyRow(),
            GlobalReportRow(
                "Valoracions globals",
            ),
            GlobalReportRow("Valoració global de les actuacions"),
            EmptyRow(),
            TitleRow("Organització"),
            GlobalReportRow(
                "La durada ha estat l'adequada?",
                values_dict=averages,
                values_dict_field="duration__avg",
            ),
            GlobalReportRow(
                "Els horaris han estat adequats?",
            ),
            GlobalReportRow(
                "Informació necessària per fer l'activitat",
            ),
            GlobalReportRow(
                "S'han complert les dates, horaris, etc...",
            ),
            GlobalReportRow(
                "Els espais han estat adequats (sales, aules, plataforma digital...)",
            ),
            EmptyRow(),
            TitleRow("Continguts"),
            GlobalReportRow(
                "Els continguts han estat adequats",
            ),
            GlobalReportRow(
                "Metodologia",
            ),
            GlobalReportRow(
                "La metodologia ha estat coherent amb els objectius",
            ),
            GlobalReportRow(
                "La metodologia ha permès obtenir millors resultats",
            ),
            GlobalReportRow(
                "El sistema de participació i resolució de dubtes ha estat adequat?",
            ),
            EmptyRow(),
            TitleRow("Valoració de la persona formadora"),
            GlobalReportRow(
                "Ha mostrat coneixements i experiència sobre el tema?",
            ),
            GlobalReportRow(
                "Ha aconseguit resoldre els problemes i dubtes que s’ha plantejat?",
            ),
            GlobalReportRow(
                "El professional ha mostrat competències comunicatives?",
            ),
            EmptyRow(),
            TitleRow("Utilitat del curs"),
            GlobalReportRow(
                "Ha satisfet les meves expectatives",
            ),
            GlobalReportRow(
                "He incorporat eines per aplicar a nous projectes",
            ),
            GlobalReportRow(
                "M'ha permès conèixer persones afins",
            ),
            GlobalReportRow(
                "Abans del curs, teníeu ganes/necessitats d'engegar algun projecte cooperatiu",
            ),
            GlobalReportRow(
                "I després?",
            ),
            EmptyRow(),
            TitleRow("Valoració global"),
            GlobalReportRow(
                "Grau de satisfacció general",
            ),
        ]

        for row in rows:
            self.export_manager.row_number += 1
            self.export_manager.fill_row_data(row.get_columns())

    def import_organizers(self):
        orgs = Organizer.objects.all()
        i = 0
        for org in orgs:
            self.organizers.update({
                i: org
            })
            i += 1
