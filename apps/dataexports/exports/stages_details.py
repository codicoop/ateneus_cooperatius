import numbers
from pprint import pprint

from django.db.models import Sum, Q, Count

from coopolis.models import ProjectStage
from coopolis.models.projects import ProjectStageSession
from dataexports.exports.manager import ExcelExportManager


class ExportStagesDetails:
    circles_data = None
    users_data = None

    def __init__(self, export_obj):
        self.export_manager = ExcelExportManager(export_obj)
        self.circles_data = CirclesDataManager(
            self.export_manager.subsidy_period
        ).get_circles_data()
        self.users_data = CirclesPerUserDataManager(
            self.export_manager.subsidy_period
        ).get_data()

    def export(self):
        """ Each function here called handles the creation of one of the
        worksheets."""
        self.export_circles()
        # self.export_axis()

        return self.export_manager.return_document("detalls_acompanyaments")

    def export_circles(self):
        self.export_manager.worksheet.title = "Ateneu-Cercles"
        self.export_manager.row_number = 1

        columns = [
            ("Ateneu", 40),
            ("Bases Convo", 20),
            ("Justificades BO", 20),
            ("Sense certificat BO", 20),
        ]
        self.export_manager.create_columns(columns)
        self.circles_ateneu_rows()
        self.circles_circle1_rows()
        self.circles_circle2_rows()
        self.circles_ateneu_user_rows()

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

    def circles_ateneu_user_rows(self):
        for data in self.users_data.values():
            pprint(data)
            verbose_name, values = data.values()
            pprint(values)
            self.export_manager.row_number += 2
            row = [
                verbose_name,
                "Número de SESSIONS",
                "Hores justificades",
                "Hores sense certificat",
            ]
            self.export_manager.row_number += 1
            self.export_manager.fill_row_data(row)
            self.export_manager.format_row_header()

            for row in values:
                self.export_manager.row_number += 1
                self.export_manager.fill_row_data(row)


class StageDetailsDataManager:
    organizer_ateneu_id = 5
    organizer_circle_migrations_id = 2
    organizer_circle_eco_id = 6
    subsidy_period = None

    def __init__(self, subsidy_period):
        self.subsidy_period = subsidy_period

    @staticmethod
    def none_as_zero(value):
        return value if value else 0


class CirclesPerUserDataManager(StageDetailsDataManager):
    def get_data(self):
        query = {
            'sessions_number': Count('session_responsible'),
            'hours_ateneu_certified': Sum(
                'hours',
                filter=(
                    Q(project_stage__stage_organizer=self.organizer_ateneu_id) &
                    Q(project_stage__scanned_certificate__isnull=False) &
                    ~Q(project_stage__scanned_certificate__exact='')
                )
            ),
            'hours_ateneu_uncertified': Sum(
                'hours',
                filter=(
                    Q(project_stage__stage_organizer=self.organizer_ateneu_id) &
                    Q(project_stage__scanned_certificate__isnull=True) |
                    Q(project_stage__scanned_certificate__exact='')
                )
            ),
            'hours_circle_migrations_certified': Sum(
                'hours',
                filter=(
                    Q(project_stage__stage_organizer=self.organizer_circle_migrations_id) &
                    Q(project_stage__scanned_certificate__isnull=False) &
                    ~Q(project_stage__scanned_certificate__exact='')
                )
            ),
            'hours_circle_migrations_uncertified': Sum(
                'hours',
                filter=(
                    Q(project_stage__stage_organizer=self.organizer_circle_migrations_id) &
                    Q(project_stage__scanned_certificate__isnull=True) |
                    Q(project_stage__scanned_certificate__exact='')
                )
            ),
            'hours_circle_eco_certified': Sum(
                'hours',
                filter=(
                    Q(project_stage__stage_organizer=self.organizer_circle_eco_id) &
                    Q(project_stage__scanned_certificate__isnull=False) &
                    ~Q(project_stage__scanned_certificate__exact='')
                )
            ),
            'hours_circle_eco_uncertified': Sum(
                'hours',
                filter=(
                    Q(project_stage__stage_organizer=self.organizer_circle_eco_id) &
                    Q(project_stage__scanned_certificate__isnull=True) |
                    Q(project_stage__scanned_certificate__exact='')
                )
            ),
        }
        qs = ProjectStageSession.objects.filter(
            project_stage__subsidy_period=self.subsidy_period,
        )
        qs = (
            qs
                .values('session_responsible__first_name')
                .annotate(**query)
        )
        qs = qs.order_by()
        data = self.format_data(qs)
        return data

    @staticmethod
    def get_base_data_structure():
        return {
            "ateneu": {
                "verbose_name": "Ateneu",
                "values": [],
            },
            "circle_migrations": {
                "verbose_name": "Cercles migracions",
                "values": [],
            },
            "circle_eco": {
                "verbose_name": "Cercles transició eco-social",
                "values": [],
            },
        }

    def fill_user_data(self, circle, item):
        return [
            item["session_responsible__first_name"],
            self.none_as_zero(
                item["sessions_number"]
            ),
            self.none_as_zero(
                item[f"hours_{circle}_certified"]
            ),
            self.none_as_zero(
                item[f"hours_{circle}_uncertified"]
            ),
        ]

    def format_data(self, data):
        base_template = self.get_base_data_structure()
        circles = [x for x in base_template.keys()]
        for item in data:
            for circle in circles:
                base_template[circle]["values"].append(
                    self.fill_user_data(circle, item)
                )
        return base_template


class CirclesDataManager(StageDetailsDataManager):
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
                    Q(stage_organizer=self.organizer_ateneu_id) &
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
                    Q(stage_organizer=self.organizer_circle_migrations_id) &
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
                    Q(stage_organizer=self.organizer_circle_eco_id) &
                    Q(scanned_certificate__isnull=True) |
                    Q(scanned_certificate__exact='')
                )
            ),
        }
        qs = ProjectStage.objects.filter(
            subsidy_period=self.subsidy_period,
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

    def format_circles_data(self, data):
        template = self.get_data_structure()
        for item in data:
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
