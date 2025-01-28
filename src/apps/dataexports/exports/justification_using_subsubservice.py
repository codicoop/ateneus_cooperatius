from dataclasses import dataclass
from enum import StrEnum

from celery.utils.collections import OrderedDict
from django.db.models import Q
from icecream import ic

from apps.cc_courses.choices import ProjectStageStatesChoices, StageTypeChoices
from apps.coopolis.choices import CirclesChoices
from apps.coopolis.models import ProjectStage, EmploymentInsertion
from apps.cc_courses.models import Activity
from apps.coopolis.models.projects import CreatedEntity
from apps.dataexports.exports.manager import ExcelExportManager
from apps.dataexports.exports.row_factories import BaseRow


@dataclass
class ActuacioRow(BaseRow):
    service: str
    subservice: str
    actuacio_name: str
    actuacio_date: str
    actuacio_period: str
    actuacio_entity: str
    circle: str
    town: str
    participants_count: int
    divulgation_material: str
    value_if_empty: str = "-"

    def get_columns(self) -> list:
        return [
            self.service or self.value_if_empty,
            self.subservice or self.value_if_empty,
            self.actuacio_name or self.value_if_empty,
            self.actuacio_date or self.value_if_empty,
            self.actuacio_period or self.value_if_empty,
            self.actuacio_entity or self.value_if_empty,
            self.circle or self.value_if_empty,
            self.town or self.value_if_empty,
            self.participants_count or self.value_if_empty,
            self.divulgation_material or self.value_if_empty,
        ]


@dataclass
class ParticipantRow(BaseRow):
    actuacio_reference: str
    user_surname: str
    user_name: str
    user_id_number: str
    user_gender: str
    user_birthdate: str
    user_town: str
    value_if_empty = "-"

    def get_columns(self) -> list:
        return [
            self.actuacio_reference or self.value_if_empty,
            "",  # Activity name: we need it empty, the excel will fill it
            self.user_surname or self.value_if_empty,
            self.user_name or self.value_if_empty,
            self.user_id_number or self.value_if_empty,
            self.user_gender or self.value_if_empty,
            self.user_birthdate or self.value_if_empty,
            self.user_town or self.value_if_empty,
        ]


@dataclass
class SessionMinorRow(BaseRow):
    actuacio_reference: str
    grade: str
    school_name: str
    participants_number: str
    value_if_empty = "-"

    def get_columns(self) -> list:
        return [
            self.actuacio_reference or self.value_if_empty,
            "",  # Activity name: we need it empty, the excel will fill it
            self.grade or self.value_if_empty,
            self.school_name or self.value_if_empty,
            self.participants_number or self.value_if_empty,
        ]


class ExportJustificationUsingSubSubService:
    """
    Aquesta classe NO fa servir cap funcionalitat relacionada amb els
    documents de correlacions (correlations_2021_2022.json etc.).
    Per tant, si en un futur es desactiven les exportacions antigues,
    es podrà eliminar tot lo relatiu a les correlacions de ExcelExportManager.
    """
    def __init__(self, export_obj):
        self.export_manager = ExcelExportManager(
            export_obj,
        )
        self.subsidy_period_range = (
            export_obj.subsidy_period.range
        )
        self.sessions_obj = self.get_sessions_obj()
        self.menors_obj = self.get_sessions_obj(for_minors=True)
        self.insercionslaborals_obj = EmploymentInsertion.objects.filter(
            subsidy_period__date_start__range=self.export_manager.subsidy_period_range,
        )
        self.stages_obj = self.get_acompanyaments_obj()
        self.acompanyaments_creacio = self.get_acompanyaments_creacio_obj()
        # PENDENT de comprovar si fent el filtre així funciona bé.
        # Sinó, caldrà fer al revés i fer un .exclude dels tipus que no volem,
        # o bé passar paràmetre com fem amb for_minors.
        self.acompanyaments_consolidacio = self.stages_obj.filter(
            stage_type=StageTypeChoices.CONSOLIDATION,
        )
        self.actuacions_obj = Actuacions()

        # 1. Omplim Actuacions amb Activities per adults (amb inscripcions)
        self.fill_actuacions_with_session_obj()

        # 2.1. Omplim Actuacions amb Acompanyaments de Creació
        self.fill_actuacions_with_acompanyaments_creacio()

        # 2.2. Omplim Actuacions amb Acompanyaments de Creació
        self.fill_actuacions_with_acompanyaments_consolidacio()

        # 3. Omplim Actuacions amb Activities per menors
        self.fill_actuacions_with_sessions_menors()

    def export(self):
        """ Each function here called handles the creation of one of the
        worksheets."""
        self.sheet_actuacions()
        self.sheet_participants()
        self.sheet_menors()

        return self.export_manager.return_document("justificacio")

    def sheet_actuacions(self):
        # The first sheet is already created, just need to adjust name.
        self.export_manager.worksheet.title = "Actuacions"
        self.export_manager.row_number = 1

        columns = [
            ("Servei", 40),
            ("Subservei", 70),
            ("Nom de l'actuació", 70),
            ("Data inici d'actuació", 16),
            ("Període d'actuacions", 16),
            ("Entitat que realitza l'actuació", 16),
            ("Cercle / Ateneu", 16),
            ("Municipi", 30),
            ("Nombre de participants", 20),
            ("Material de difusió (S/N)", 21),
            ("[Document acreditatiu]", 21),
            ("[Incidències]", 20),
            ("[Lloc]", 20),
            ("[Acció]", 20),
            ("[Cofinançat]", 20),
            ("[Cofinançat amb AACC]", 20),
            ("[Ateneu/Cercle]", 20),
            ("[Línia estratègica]", 20),
            ("[Link]", 20),
        ]
        self.export_manager.create_columns(columns)
        self.rows_actuacions()

    def rows_actuacions(self):
        for row in self.actuacions_obj.rows.values():
            self.export_manager.fill_row_from_factory(row.row_data)

    def fill_actuacions_with_session_obj(self):
        for item in self.sessions_obj:
            service = ""
            subservice = ""
            if item.subsubservice:
                service = item.subsubservice.subservice.service.name
                subservice = item.subsubservice.subservice.name
            circle = (
                CirclesChoices(item.circle).label
                if item.circle is not None
                else ""
            )
            town = ""
            if item.place is not None and item.place.town:
                town = item.place.town.name
            divulgation_material = "No"
            if item.photo2.name:
                divulgation_material = "Sí"
            row = ActuacioRow(
                service=service,
                subservice=subservice,
                actuacio_name=item.name,
                actuacio_date=item.date_start,
                actuacio_period="",
                actuacio_entity=str(item.entity) if item.entity else "",
                circle=circle,
                town=town,
                participants_count=item.enrolled.count(),
                divulgation_material=divulgation_material,
            )
            self.actuacions_obj.add_row(
                group=Actuacions.GROUPS.ACTIVITY.value,
                id=item.pk,
                actuacio_row_obj=row,
            )

    def fill_actuacions_with_acompanyaments_creacio(self):
        for item in self.acompanyaments_creacio:
            item = item.project_stage
            service = ""
            subservice = ""
            if item.subsubservice:
                service = item.subsubservice.subservice.service.name
                subservice = item.subsubservice.subservice.name
            circle = (
                CirclesChoices(item.circle).label
                if item.circle is not None
                else ""
            )
            town = ""
            if item.project.town:
                town = item.project.town.name
            row = ActuacioRow(
                service=service,
                subservice=subservice,
                actuacio_name=item.project.name,
                actuacio_date=item.earliest_session.date if item.earliest_session else "",
                actuacio_period="",
                actuacio_entity=item.entities_str,
                circle=circle,
                town=town,
                participants_count=len(item.partners_involved_in_sessions),
                divulgation_material="No",
            )
            self.actuacions_obj.add_row(
                group=Actuacions.GROUPS.CREATION.value,
                id=item.pk,
                actuacio_row_obj=row,
            )

    def fill_actuacions_with_acompanyaments_consolidacio(self):
        for item in self.acompanyaments_consolidacio:
            service = ""
            subservice = ""
            if item.subsubservice:
                service = item.subsubservice.subservice.service.name
                subservice = item.subsubservice.subservice.name
            circle = (
                CirclesChoices(item.circle).label
                if item.circle is not None
                else ""
            )
            town = ""
            if item.project.town:
                town = item.project.town.name
            row = ActuacioRow(
                service=service,
                subservice=subservice,
                actuacio_name=item.project.name,
                actuacio_date=item.earliest_session.date if item.earliest_session else "",
                actuacio_period="",
                actuacio_entity=item.entities_str,
                circle=circle,
                town=town,
                participants_count=len(item.partners_involved_in_sessions),
                divulgation_material="No",
            )
            self.actuacions_obj.add_row(
                group=Actuacions.GROUPS.CONSOLIDATION.value,
                id=item.pk,
                actuacio_row_obj=row,
            )

    def fill_actuacions_with_sessions_menors(self):
        for item in self.menors_obj:
                service = ""
                subservice = ""
                if item.subsubservice:
                    service = item.subsubservice.subservice.service.name
                    subservice = item.subsubservice.subservice.name
                circle = (
                    CirclesChoices(item.circle).label
                    if item.circle is not None
                    else ""
                )
                town = ""
                if item.place is not None and item.place.town:
                    town =item.place.town.name
                divulgation_material = "No"
                if item.photo2.name:
                    divulgation_material = "Sí"
                row = ActuacioRow(
                    service=service,
                    subservice=subservice,
                    actuacio_name=item.name,
                    actuacio_date=item.date_start,
                    actuacio_period="",
                    actuacio_entity=str(item.entity) if item.entity else "",
                    circle=circle,
                    town=town,
                    participants_count=item.enrolled.count(),
                    divulgation_material=divulgation_material,
                )
                self.actuacions_obj.add_row(
                    group=Actuacions.GROUPS.ACTIVITY_MINORS.value,
                    id=item.pk,
                    actuacio_row_obj=row,
                )

    def sheet_participants(self):
        self.export_manager.worksheet = self.export_manager.workbook.create_sheet(
            "Participants",
        )
        self.export_manager.row_number = 1

        columns = [
            ("Referència", 40),
            ("Nom actuació", 40),
            ("Cognoms", 20),
            ("Nom", 10),
            ("Doc. identificatiu", 12),
            ("Gènere", 10),
            ("Data naixement", 10),
            ("Municipi del participant", 20),
            ("[Situació laboral]", 20),
            ("[Procedència]", 20),
            ("[Nivell d'estudis]", 20),
            ("[Com ens has conegut]", 20),
            ("[Email]", 30),
            ("[Telèfon]", 30),
            ("[Projecte]", 30),
            ("[Acompanyaments]", 30),
        ]
        self.export_manager.create_columns(columns)

        self.fill_participants_from_sessions()
        self.fill_participants_from_acompanyaments_creacio()
        self.fill_participants_from_acompanyaments_consolidacio()

    def fill_participants_from_sessions(self):
        for activity in self.sessions_obj:
            for enrollment in activity.enrollments.all():
                # Originally we queried activity.confirmed_enrollments, but to
                # optimize performance, we loop all activity.enrollments and
                # ignore the ones in waiting list.
                # That way we're not making a new DB query for each activity.
                if enrollment.waiting_list:
                    continue
                participant = enrollment.user
                actuacio_obj = self.actuacions_obj.rows[
                    (self.actuacions_obj.GROUPS.ACTIVITY.value, activity.id)
                ]
                town = ""
                if participant.town:
                    town = participant.town.name
                row = ParticipantRow(
                    actuacio_reference=actuacio_obj.reference,
                    user_surname=participant.surname,
                    user_name=participant.first_name,
                    user_id_number=participant.id_number,
                    user_gender=participant.get_gender_display() or "",
                    user_birthdate=participant.birthdate or "",
                    user_town=town,
                )
                self.export_manager.fill_row_from_factory(row)

    def fill_participants_from_acompanyaments_creacio(self):
        for created_entity_obj in self.acompanyaments_creacio:
            project_stage = created_entity_obj.project_stage
            actuacio_obj = self.actuacions_obj.rows[
                (self.actuacions_obj.GROUPS.CREATION.value, project_stage.id)
            ]
            for participant in project_stage.partners_involved_in_sessions:
                town = ""
                if participant.town:
                    town = participant.town.name
                row = ParticipantRow(
                    actuacio_reference=actuacio_obj.reference,
                    user_surname=participant.surname,
                    user_name=participant.first_name,
                    user_id_number=participant.id_number,
                    user_gender=participant.get_gender_display() or "",
                    user_birthdate=participant.birthdate or "",
                    user_town=town,
                )
                self.export_manager.fill_row_from_factory(row)


    def fill_participants_from_acompanyaments_consolidacio(self):
        for project_stage in self.acompanyaments_consolidacio:
            actuacio_obj = self.actuacions_obj.rows[
                (self.actuacions_obj.GROUPS.CONSOLIDATION.value, project_stage.id)
            ]
            for participant in project_stage.partners_involved_in_sessions:
                town = ""
                if participant.town:
                    town = participant.town.name
                row = ParticipantRow(
                    actuacio_reference=actuacio_obj.reference,
                    user_surname=participant.surname,
                    user_name=participant.first_name,
                    user_id_number=participant.id_number,
                    user_gender=participant.get_gender_display() or "",
                    user_birthdate=participant.birthdate or "",
                    user_town=town,
                )
                self.export_manager.fill_row_from_factory(row)

    def sheet_menors(self):
        self.export_manager.worksheet = self.export_manager.workbook.create_sheet(
            "Menors",
        )
        self.export_manager.row_number = 1

        columns = [
            ("Referència", 40),
            ("Nom actuació", 40),
            ("Grau d'estudis", 20),
            ("Nom centre educatiu", 20),
            ("Nombre participants", 20),
        ]
        self.export_manager.create_columns(columns)

        self.fill_menors()

    def fill_menors(self):
        for activity in self.menors_obj:
            actuacio_obj = self.actuacions_obj.rows[
                (self.actuacions_obj.GROUPS.ACTIVITY_MINORS.value, activity.id)
            ]
            row = SessionMinorRow(
                actuacio_reference=actuacio_obj.reference,
                grade=activity.get_minors_grade_display(),
                school_name=activity.minors_school_name,
                participants_number=activity.minors_participants_number,
            )
            self.export_manager.fill_row_from_factory(row)

    def get_sessions_obj(self, for_minors=False):
        return Activity.objects.filter(
            Q(
                date_start__range=self.export_manager.subsidy_period.range,
                for_minors=for_minors,
            ) & (
                Q(cofunded__isnull=True) | (
                    Q(cofunded__isnull=False) & Q(cofunded_ateneu=True)
                )
            )
        ).exclude(
            exclude_from_justification=True,
        )

    def get_acompanyaments_obj(self):
        return ProjectStage.objects.order_by("date_start").filter(
            Q(
                subsidy_period=self.export_manager.subsidy_period
            ) & Q(
                exclude_from_justification=False
            ) & (
                Q(cofunded__isnull=True) | (
                    Q(cofunded__isnull=False) & Q(cofunded_ateneu=True)
                )
            )
        ).exclude(
            Q(stage_sessions__isnull=True)
            | Q(stage_state=ProjectStageStatesChoices.PENDING)
        )

    def get_acompanyaments_creacio_obj(self):
        return CreatedEntity.objects.filter(
            Q(
                project_stage__subsidy_period=self.export_manager.subsidy_period
            ) & Q(
                project_stage__exclude_from_justification=False
            ) & (
                Q(
                    project_stage__cofunded__isnull=True
                ) | (
                    Q(
                        project_stage__cofunded__isnull=False
                    ) & Q(
                        project_stage__cofunded_ateneu=True
                    )
                )
            )
        ).exclude(
            # Pels casos d'ateneus que no van fer bé la tasca
            # d'assignar un acompanyament a tots els registres d'entitats
            # creades.
            project_stage__isnull=True,
        )


@dataclass
class Actuacio:
    row_number: int
    reference: str
    id: str
    group: str
    row_data: str

class Groups(StrEnum):
    ACTIVITY = "activity"
    ACTIVITY_MINORS = "activity_minors"
    CONSOLIDATION = "consolidation"
    CREATION = "creation"

class Actuacions:
    GROUPS = Groups

    def __init__(self):
        # OrderedDict will remember the order that the items were added
        self.rows = OrderedDict()
        self.last_row = 0

    def get_row(self, group, id):
        pass

    def add_row(self, group, id, actuacio_row_obj):
        """
        :param group: one of self.GROUPS
        :param id: The row's item database ID
        :param actuacio_row_obj: An ActuacioRow instance
        :return: The newly created and added Actuacio object
        """
        if (group, id) in self.rows:
            raise ValueError(f"Row with ID {id} already exists in group "
                             f"{group.value}")
        self.last_row += 1
        reference = self.get_formatted_reference(
            row_number=self.last_row,
            subservice=actuacio_row_obj.subservice,
            actuacio_entity=actuacio_row_obj.actuacio_entity,
            circle=actuacio_row_obj.circle,
            actuacio_period=actuacio_row_obj.actuacio_period,
        )
        actuacio_obj = Actuacio(
            row_number=self.last_row,
            reference=reference,
            id=id,
            group=group,
            row_data=actuacio_row_obj,
        )
        self.rows[(group, id)] = actuacio_obj

    @staticmethod
    def get_formatted_reference(
        row_number,
        subservice,
        actuacio_entity,
        circle,
        actuacio_period,
    ):
        if (
            not subservice 
            or not actuacio_entity
            or not circle 
            or not actuacio_period 
        ):
            return ""
        return (
            f"{row_number} - {subservice} {actuacio_period} {actuacio_entity} - {circle}"
        )
