from pprint import pprint

from django.db.models import Count, Avg, F, IntegerField, Case, When, Sum, \
    Value

from cc_courses.models import Organizer
from coopolis.models import ActivityPoll
from dataexports.exports.manager import ExcelExportManager


class BaseRow:
    def get_columns(self) -> list:
        return []


class GlobalReportYesNoEmptyRow(BaseRow):
    def __init__(
        self,
        title: str,
        ateneu: tuple = (),
        cercle1: tuple = (),
        cercle2: tuple = (),
        cercle3: tuple = (),
        cercle4: tuple = (),
    ):
        self.title = title
        self.ateneu = self.to_yes_no_empty(ateneu)
        self.cercle1 = self.to_yes_no_empty(cercle1)
        self.cercle2 = self.to_yes_no_empty(cercle2)
        self.cercle3 = self.to_yes_no_empty(cercle3)
        self.cercle4 = self.to_yes_no_empty(cercle4)

    def to_yes_no_empty(self, values):
        if len(values) == 3:
            return f"Sí {values[0]}, No {values[1]}, Blanc {values[2]}"
        return "-"

    def get_columns(self) -> list:
        return [
            self.title,
            self.ateneu,
            self.cercle1,
            self.cercle2,
            self.cercle3,
            self.cercle4,
        ]


class GlobalReportRow(BaseRow):
    value_if_empty = "-"

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
            self.ateneu = values_dict["ateneu"].get(values_dict_field)
            self.cercle1 = values_dict["cercle1"].get(values_dict_field)
            self.cercle2 = values_dict["cercle2"].get(values_dict_field)
            self.cercle3 = values_dict["cercle3"].get(values_dict_field)
            self.cercle4 = values_dict["cercle4"].get(values_dict_field)

    def get_columns(self) -> list:
        return [
            self.title,
            round(self.ateneu, 1) if self.ateneu else self.value_if_empty,
            round(self.cercle1, 1) if self.cercle1 else self.value_if_empty,
            round(self.cercle2, 1) if self.cercle2 else self.value_if_empty,
            round(self.cercle3, 1) if self.cercle3 else self.value_if_empty,
            round(self.cercle4, 1) if self.cercle4 else self.value_if_empty,
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
            Avg("teacher_has_knowledge"),
            Avg("teacher_resolved_doubts"),
            Avg("teacher_has_communication_skills"),
            Avg("expectations_satisfied"),
            Avg("adquired_new_tools"),
            # Avg("wanted_start_cooperative"),
            # Avg("wants_start_cooperative_now"),
            Avg("general_satisfaction"),
            met_new_people_yes=Sum(
                Case(
                    When(met_new_people=True, then=Value(1)),
                    output_field=IntegerField(),
                    default=0,
                )
            ),
            met_new_people_no=Sum(
                Case(
                    When(met_new_people=False, then=Value(1)),
                    output_field=IntegerField(),
                    default=0,
                ),
            ),
            met_new_people_empty=Sum(
                Case(
                    When(met_new_people=None, then=Value(1)),
                    output_field=IntegerField(),
                    default=0,
                )
            ),
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
                values_dict=averages,
                values_dict_field="hours__avg",
            ),
            GlobalReportRow(
                "Informació necessària per fer l'activitat",
                values_dict=averages,
                values_dict_field="information__avg",
            ),
            GlobalReportRow(
                "S'han complert les dates, horaris, etc...",
                values_dict=averages,
                values_dict_field="on_schedule__avg",
            ),
            GlobalReportRow(
                "Materials de suport facilitats",
                values_dict=averages,
                values_dict_field="included_resources__avg",
            ),
            GlobalReportRow(
                "Els espais han estat adequats (sales, aules, plataforma digital...)",
                values_dict=averages,
                values_dict_field="space_adequation__avg",
            ),
            EmptyRow(),
            TitleRow("Continguts"),
            GlobalReportRow(
                "Els continguts han estat adequats",
                values_dict=averages,
                values_dict_field="contents__avg",
            ),
            TitleRow("Metodologia"),
            GlobalReportRow(
                "La metodologia ha estat coherent amb els objectius",
                values_dict=averages,
                values_dict_field="methodology_fulfilled_objectives__avg",
            ),
            GlobalReportRow(
                "La metodologia ha permès obtenir millors resultats",
                values_dict=averages,
                values_dict_field="methodology_better_results__avg",
            ),
            GlobalReportRow(
                "El sistema de participació i resolució de dubtes ha estat adequat?",
                values_dict=averages,
                values_dict_field="participation_system__avg",
            ),
            EmptyRow(),
            TitleRow("Valoració de la persona formadora"),
            GlobalReportRow(
                "Ha mostrat coneixements i experiència sobre el tema?",
                values_dict=averages,
                values_dict_field="teacher_has_knowledge__avg",
            ),
            GlobalReportRow(
                "Ha aconseguit resoldre els problemes i dubtes que s’ha plantejat?",
                values_dict=averages,
                values_dict_field="teacher_resolved_doubts__avg",
            ),
            GlobalReportRow(
                "El professional ha mostrat competències comunicatives?",
                values_dict=averages,
                values_dict_field="teacher_has_communication_skills__avg",
            ),
            EmptyRow(),
            TitleRow("Utilitat del curs"),
            GlobalReportRow(
                "Ha satisfet les meves expectatives",
                values_dict=averages,
                values_dict_field="expectations_satisfied__avg",
            ),
            GlobalReportRow(
                "He incorporat eines per aplicar a nous projectes",
                values_dict=averages,
                values_dict_field="adquired_new_tools__avg",
            ),
            GlobalReportYesNoEmptyRow(
                "M'ha permès conèixer persones afins",
                (
                    averages["ateneu"].get("met_new_people_yes"),
                    averages["ateneu"].get("met_new_people_no"),
                    averages["ateneu"].get("met_new_people_empty"),
                ),
                (
                    averages["cercle1"].get("met_new_people_yes"),
                    averages["cercle1"].get("met_new_people_no"),
                    averages["cercle1"].get("met_new_people_empty"),
                ),
                (
                    averages["cercle2"].get("met_new_people_yes"),
                    averages["cercle2"].get("met_new_people_no"),
                    averages["cercle2"].get("met_new_people_empty"),
                ),
                (
                    averages["cercle3"].get("met_new_people_yes"),
                    averages["cercle3"].get("met_new_people_no"),
                    averages["cercle3"].get("met_new_people_empty"),
                ),
                (
                    averages["cercle4"].get("met_new_people_yes"),
                    averages["cercle4"].get("met_new_people_no"),
                    averages["cercle4"].get("met_new_people_empty"),
                ),
            ),
            GlobalReportRow(
                "Abans del curs, teníeu ganes/necessitats d'engegar algun projecte cooperatiu",
                values_dict=averages,
                values_dict_field="wanted_start_cooperative__avg",
            ),
            GlobalReportRow(
                "I després?",
                values_dict=averages,
                values_dict_field="wants_start_cooperative_now__avg",
            ),
            EmptyRow(),
            TitleRow("Valoració global"),
            GlobalReportRow(
                "Grau de satisfacció general",
                values_dict=averages,
                values_dict_field="general_satisfaction__avg",
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
