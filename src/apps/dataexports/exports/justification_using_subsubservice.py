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
        self.nouniversitaris_obj = self.get_sessions_obj(for_minors=True)
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
        self.acompanyaments_incubacio = self.stages_obj.filter(
            stage_type=StageTypeChoices.INCUBATION,
        )
        self.actuacions_obj = Actuacions()

        # 1. Omplim Actuacions amb Activities per adults (amb inscripcions)
        self.fill_actuacions_with_session_obj()

        # 2.1. Omplim Actuacions amb Acompanyaments de Creació
        self.fill_actuacions_with_acompanyaments_creacio()

        # 2.2. Omplim Actuacions amb Acompanyaments de Creació
        self.fill_actuacions_with_acompanyaments_consolidacio()

        # 2.3. Omplim Actuacions amb Acompanyaments d'Incubació
        self.fill_actuacions_with_acompanyaments_incubacio()

        # 3. Omplim Actuacions amb Activities per menors
        self.fill_actuacions_with_sessions_menors()

        ic(self.actuacions_obj.rows)

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
                group=Actuacions.GROUPS.ACTIVITY,
                id=item.pk,
                actuacio_row_obj=row,
            )

    def fill_actuacions_with_acompanyaments_creacio(self):
        for item in self.acompanyaments_creacio:
            if not getattr(item, "project_stage") or not item.project_stage:
                # Si això passa són casos d'ateneus que no van fer bé la tasca
                # d'assignar un acompanyament a tots els registres d'entitats
                # creades.
                continue
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
                group=Actuacions.GROUPS.CREATION,
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
                group=Actuacions.GROUPS.CONSOLIDATION,
                id=item.pk,
                actuacio_row_obj=row,
            )

    def fill_actuacions_with_acompanyaments_incubacio(self):
        for item in self.acompanyaments_incubacio:
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
                group=Actuacions.GROUPS.INCUBATION,
                id=item.pk,
                actuacio_row_obj=row,
            )

    def fill_actuacions_with_sessions_menors(self):
        for item in self.nouniversitaris_obj:
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
                    group=Actuacions.GROUPS.ACTIVITY_MINORS,
                    id=item.pk,
                    actuacio_row_obj=row,
                )

    def export(self):
        """ Each function here called handles the creation of one of the
        worksheets."""
        # self.export_actuacions()

        return self.export_manager.return_document("justificacio")

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
    INCUBATION = "incubation"
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
