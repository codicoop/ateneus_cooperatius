import numbers
from pprint import pprint

from django.db.models import Sum, Q

from coopolis.models import ProjectStage
from dataexports.exports.manager import ExcelExportManager


class ExportStagesDetails:
    organizer_ateneu_id = 5
    organizer_circle_migrations_id = 2
    organizer_circle_eco_id = 6
    circles_data = None

    def __init__(self, export_obj):
        self.export_manager = ExcelExportManager(export_obj)
        self.circles_data = self.get_circles_data()

    def export(self):
        """ Each function here called handles the creation of one of the
        worksheets."""
        self.export_circles()
        # self.export_axis()

        return self.export_manager.return_document("detalls_acompanyaments")

    def export_circles(self):
        self.export_manager.worksheet.title = "Acompanyaments covid"
        self.export_manager.row_number = 1

        columns = [
            ("Ateneu", 40),
            ("Bases Convo", 20),
            ("Justificades BO", 20),
            ("Sense certificat BO", 20),
        ]
        self.export_manager.create_columns(columns)

        self.circles_rows()

    def get_axis_key(self, axis, qs):
        for key, value in qs:
            if value['axis'] == axis:
                return key
        return None

    @staticmethod
    def none_as_zero(value):
        return value if value else 0

    def format_circles_data(self, data):
        template = self.get_data_structure()
        for item in data:
            print("Item:")
            pprint(item["hours_ateneu_certified"])
            # Ateneu
            template["ateneu"][item["axis"]][2] = self.none_as_zero(
                item["hours_ateneu_certified"]
            )
            template["ateneu"][item["axis"]][3] = self.none_as_zero(
                item["hours_ateneu_uncertified"]
            )
            if isinstance(item["hours_ateneu_certified"], numbers.Number):
                template["ateneu"]["total"][2] += item["hours_ateneu_certified"]
            if isinstance(item["hours_ateneu_uncertified"], numbers.Number):
                template["ateneu"]["total"][3] += item["hours_ateneu_uncertified"]

            # Cercle Migracions
            template["circle_migrations"][item["axis"]][2] = self.none_as_zero(
                item["hours_circle_migrations_certified"]
            )
            template["circle_migrations"][item["axis"]][3] = self.none_as_zero(
                item["hours_circle_migrations_uncertified"]
            )
            if isinstance(item["hours_circle_migrations_certified"], numbers.Number):
                template["circle_migrations"]["total"][2] += \
                    item["hours_circle_migrations_certified"]
            if isinstance(item["hours_circle_migrations_uncertified"], numbers.Number):
                template["circle_migrations"]["total"][3] += \
                    item["hours_circle_migrations_uncertified"]

            # Cercle canvi ecosocial
            template["circle_eco"][item["axis"]][2] = self.none_as_zero(
                item["hours_circle_eco_certified"]
            )
            template["circle_eco"][item["axis"]][3] = self.none_as_zero(
                item["hours_circle_eco_uncertified"]
            )
            if isinstance(item["hours_circle_eco_certified"], numbers.Number):
                template["circle_eco"]["total"][2] += \
                    item["hours_circle_eco_certified"]
            if isinstance(item["hours_circle_eco_uncertified"], numbers.Number):
                template["circle_eco"]["total"][3] += \
                    item["hours_circle_eco_uncertified"]
        return template

    def get_circles_data(self):
        query = {
            'hours_ateneu_certified': Sum(
                'stage_sessions__hours',
                filter=(
                    Q(stage_organizer=self.organizer_ateneu_id) &
                    Q(scanned_certificate__isnull=False) &
                    ~Q(scanned_certificate__exact='')
                )
            ),
            'hours_ateneu_uncertified': Sum(
                'stage_sessions__hours',
                filter=(
                    Q(scanned_certificate__isnull=True) |
                    Q(scanned_certificate__exact='')
                )
            ),
            'hours_circle_migrations_certified': Sum(
                'stage_sessions__hours',
                filter=(
                    Q(stage_organizer=self.organizer_circle_migrations_id) &
                    Q(scanned_certificate__isnull=False) &
                    ~Q(scanned_certificate__exact='')
                )
            ),
            'hours_circle_migrations_uncertified': Sum(
                'stage_sessions__hours',
                filter=(
                    Q(scanned_certificate__isnull=True) |
                    Q(scanned_certificate__exact='')
                )
            ),
            'hours_circle_eco_certified': Sum(
                'stage_sessions__hours',
                filter=(
                    Q(stage_organizer=self.organizer_circle_eco_id) &
                    Q(scanned_certificate__isnull=False) &
                    ~Q(scanned_certificate__exact='')
                )
            ),
            'hours_circle_eco_uncertified': Sum(
                'stage_sessions__hours',
                filter=(
                    Q(scanned_certificate__isnull=True) |
                    Q(scanned_certificate__exact='')
                )
            ),
        }
        qs = ProjectStage.objects.filter(
            subsidy_period=self.export_manager.subsidy_period,
        )
        qs = (
            qs
                .values('axis')
                .annotate(**query)
        )
        # Disabling order_by because it breaks the group_by.
        qs = qs.order_by()
        data = self.format_circles_data(qs)
        return data

    def circles_rows(self):
        self.circles_ateneu_rows()
        self.circles_circle1_rows()
        self.circles_circle2_rows()

    def circles_ateneu_rows(self):
        rows = list(self.circles_data["ateneu"].values())
        for row in rows:
            self.export_manager.row_number += 1
            self.export_manager.fill_row_data(row)

    def circles_circle1_rows(self):
        self.export_manager.row_number += 1
        row = [
            "Cercle transició eco-social",
            "Bases Convo",
            "Justificades BO",
            "Sense certificat BO",
        ]
        self.export_manager.row_number += 1
        self.export_manager.fill_row_data(row)
        self.export_manager.format_row_header()

        rows = self.circles_data["circle_migrations"].values()
        for row in rows:
            self.export_manager.row_number += 1
            self.export_manager.fill_row_data(row)

    def circles_circle2_rows(self):
        self.export_manager.row_number += 1
        row = [
            "Cercle migracions",
            "Bases Convo",
            "Justificades BO",
            "Sense certificat BO",
        ]
        self.export_manager.row_number += 1
        self.export_manager.fill_row_data(row)
        self.export_manager.format_row_header()
        rows = self.circles_data["circle_eco"].values()
        for row in rows:
            self.export_manager.row_number += 1
            self.export_manager.fill_row_data(row)

    @staticmethod
    def get_data_structure():
        return {
          "ateneu": {
            "total": [
                "Total hores",
                1000,  # Bases Convo
                0,  # Justificades
                0,  # Sense certificat
            ],
            "B": [
                "Eix B",
                "??",  # Bases Convo
                0,  # Justificades
                0,  # Sense certificat
            ],
            "C": [
                "Eix C",
                114,  # Bases Convo
                0,  # Justificades
                0,  # Sense certificat
            ],
            "D": [
                "Eix D",
                110,  # Bases Convo
                0,  # Justificades
                0,  # Sense certificat
            ],
            "insertions": [
                "Insercions",
                30,  # Bases Convo
                0,  # Justificades
                0,  # Sense certificat
            ],
            "constituted": [
                "Constitució",
                0,  # Bases Convo
                0,  # Justificades
                0,  # Sense certificat
            ],
          },
          "circle_migrations": {
            "total": [
                "Total hores",
                300,  # Bases Convo
                0,  # Justificades
                0,  # Sense certificat
            ],
            "B": [
                "Eix B",
                "??",  # Bases Convo
                0,  # Justificades
                0,  # Sense certificat
            ],
            "C": [
                "Eix C",
                1,  # Bases Convo
                0,  # Justificades
                0,  # Sense certificat
            ],
            "D": [
                "Eix D",
                "1 a 20h",  # Bases Convo
                0,  # Justificades
                0,  # Sense certificat
            ],
            "insertions": [
                "insercions",
                8,  # Bases Convo
                0,  # Justificades
                0,  # Sense certificat
            ],
            "constituted": [
                "Constitució",
                "No",  # Bases Convo
                0,  # Justificades
                0,  # Sense certificat
            ],
          },
          "circle_eco": {
            "total": [
                "Total hores",
                300,  # Bases Convo
                0,  # Justificades
                0,  # Sense certificat
            ],
            "B": [
                "Eix B",
                "??",  # Bases Convo
                0,  # Justificades
                0,  # Sense certificat
            ],
            "C": [
                "Eix C",
                1,  # Bases Convo
                0,  # Justificades
                0,  # Sense certificat
            ],
            "D": [
                "Eix C",
                "1 a 20h",  # Bases Convo
                0,  # Justificades
                0,  # Sense certificat
            ],
            "insertions": [
                "Insercions",
                8,  # Bases Convo
                0,  # Justificades
                0,  # Sense certificat
            ],
            "constituted": [
                "Constitució",
                "No",  # Bases Convo
                0,  # Justificades
                0,  # Sense certificat
            ],
          },
        }
