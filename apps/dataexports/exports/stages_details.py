import numbers
from pprint import pprint

from django.db.models import Sum, Q, Count

from coopolis.models import ProjectStage
from coopolis.models.projects import ProjectStageSession, StageSubtype
from dataexports.exports.manager import ExcelExportManager


class ExportStagesDetails:
    circles_data = None
    users_data = None
    stage_types_data = None

    def __init__(self, export_obj):
        self.export_manager = ExcelExportManager(export_obj)
        self.circles_data = CirclesDataManager(
            self.export_manager.subsidy_period
        ).get_circles_data()
        self.users_data = CirclesPerUserDataManager(
            self.export_manager.subsidy_period
        ).get_data()
        self.stage_types_data = StageTypesDataManager(
            self.export_manager.subsidy_period
        ).get_data()

    def export(self):
        """ Each function here called handles the creation of one of the
        worksheets."""
        self.export_circles()
        self.export_stage()

        return self.export_manager.return_document("detalls_acompanyaments")

    def export_stage(self):
        self.export_manager.worksheet = \
            self.export_manager.workbook.create_sheet("Itinerari")
        self.export_manager.row_number = 1

        columns = [
            ("Tipus d'acompanyament justifica.", 40),
            ("Hores executades", 20),
            ("Hores justificades", 20),
            ("Hores sense certificat", 20),
            ("Percentatge", 20),
        ]
        self.export_manager.create_columns(columns)
        self.stage_totals_rows()

    def stage_totals_rows(self):
        for row in self.stage_types_data:
            self.export_manager.row_number += 1
            self.export_manager.fill_row_data(row)

    def stage_creation_rows(self):
        self.export_manager.row_number += 1
        row = [
            "Creació - Acollida",
            "Número",
            "Hores justificades",
            "Hores sense certificat",
        ]
        self.export_manager.row_number += 1
        self.export_manager.fill_row_data(row)
        self.export_manager.format_row_header()

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
            verbose_name, values = data.values()
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


class StageTypesDataManager(StageDetailsDataManager):
    """
    stage_subtypes will be populated with this scheme:
    {1: 'Acollida', 2: 'Procés', 3: 'Constitució', 4: 'Acompanyament'}
    """
    stage_types = {
        11: {
            "verbose_name": "Creació",
            "name": "creation",
        },
        12: {
            "verbose_name": "Consolidació",
            "name": "consolidation",
        },
    }
    stage_subtypes = {}

    def __init__(self, *args):
        super().__init__(*args)
        qs = StageSubtype.objects.all()
        for subtype in qs:
            self.stage_subtypes.update({
                subtype.pk: subtype.name
            })
        pprint(self.stage_subtypes)

    def get_data(self):
        stage_creation_totals_data = self.get_totals_data(
            self.stage_types[11]
        )
        stage_consolidation_totals_data = self.get_totals_data(
            self.stage_types[12]
        )

        return stage_creation_totals_data + stage_consolidation_totals_data

    def get_totals_data(self, stage_type):
        stage_type_name = stage_type["name"]
        query = {
            f"hours_{stage_type_name}_certified": Sum(
                "stage_sessions__hours",
                filter=(
                    Q(scanned_certificate__isnull=False) &
                    ~Q(scanned_certificate__exact='')
                )
            ),
            f"hours_{stage_type_name}_uncertified": Sum(
                "stage_sessions__hours",
                filter=(
                    Q(scanned_certificate__isnull=True) |
                    Q(scanned_certificate__exact='')
                )
            ),
        }
        qs = ProjectStage.objects.filter(
            subsidy_period=self.subsidy_period,
            stage_type=11,
        )
        qs = (
            qs
                .values('stage_subtype')
                .annotate(**query)
        )
        qs = qs.order_by()
        data = self.format_totals_data(stage_type, qs)
        return data

    def format_totals_data(self, stage_type, qs):
        """
        IDEA:
        Aprofitar que el query que ja tenim ara genera totes les combinacions de:
        creation - Acollida
        creation - Procés
        creation - Constitució
        consolidation - Acollida
        consolidation - Acompanyament
        :return:
        """
        data = []
        for item in qs:
            data.append(self.fill_total_row(stage_type, item))
        pprint(data)
        return data

    def fill_total_row(self, stage_type, item):
        cert = self.none_as_zero(
            item[f"hours_{stage_type['name']}_certified"]
        )
        uncert = self.none_as_zero(
            item[f"hours_{stage_type['name']}_uncertified"]
        )
        subtype_name = self.stage_subtypes[item['stage_subtype']]
        return [
            f"{stage_type['verbose_name']} - {subtype_name}",
            cert + uncert,
            cert,
            uncert,
            0,  # TODO: Percentage
        ]


class StagePerUserDataManager(StageDetailsDataManager):
    def get_data(self):
        for stage in self.stages:
            for subtype in self.stage_subtypes:
                query = {
                    "sessions_number": Count('session_responsible'),
                    f"hours_{stage['verbose_name']}_{subtype.name}_certified": Sum(
                        'hours',
                        filter=(
                            Q(project_stage__scanned_certificate__isnull=False) &
                            ~Q(project_stage__scanned_certificate__exact='')
                        )
                    ),
                    f"hours_{stage['verbose_name']}_{subtype.name}_uncertified": Sum(
                        'hours',
                        filter=(
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
        pprint(qs)
        data = self.format_data(qs)
        return data

    @staticmethod
    def get_base_data_structure():
        data = {
            "creacio": {
                "verbose_name": "Ateneu",
                "values": [],
            },
            "consolidacio": {
                "verbose_name": "Cercles migracions",
                "values": [],
            },
        }
        return data

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
