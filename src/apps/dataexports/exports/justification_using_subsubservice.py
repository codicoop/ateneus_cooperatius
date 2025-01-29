from dataclasses import dataclass
from enum import StrEnum

from celery.utils.collections import OrderedDict
from django.db.models import Q

from apps.cc_courses.choices import ProjectStageStatesChoices, StageTypeChoices
from apps.coopolis.choices import CirclesChoices
from apps.coopolis.models import ProjectStage, EmploymentInsertion
from apps.cc_courses.models import Activity
from apps.coopolis.models.projects import CreatedEntity
from apps.dataexports.exports.manager import ExcelExportManager
from apps.dataexports.exports.row_factories import (
    ActuacioRow,
    ParticipantRow,
    SessionMinorRow,
    InsercioLaboralRow,
    CreatedEntityRow,
    AcompanyamentRow,
)


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
        self.acompanyaments_creacio = self.get_acompanyaments_creacio_obj()
        # PENDENT de comprovar si fent el filtre així funciona bé.
        # Sinó, caldrà fer al revés i fer un .exclude dels tipus que no volem,
        # o bé passar paràmetre com fem amb for_minors.
        self.acompanyaments_consolidacio = self.get_acompanyaments_obj().filter(
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
        self.sheet_insercionslaborals()
        self.sheet_created_projects()
        self.sheet_acompanyaments()

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
            ("[Lloc]", 20),
            ("[Acció]", 20),
            ("[Cofinançat]", 20),
            ("[Cofinançat amb AACC]", 20),
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
            material_difusio = "No"
            if item.file1.name:
                material_difusio = "Sí"
            document_acreditatiu = "No"
            if item.photo2.name:
                document_acreditatiu = "Sí"

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
                material_difusio=material_difusio,
                document_acreditatiu=document_acreditatiu,
                place=str(item.place) if item.place else '',
                accio=str(item.course),
                cofunded=str(item.cofunded or "No"),
                cofunded_ateneu="Sí" if item.cofunded_ateneu else "No",
                strategic_line=(
                    item.strategic_line.name if item.strategic_line else ""
                ),
                admin_url=item.absolute_url_admin,
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
                material_difusio="No",
                document_acreditatiu="",
                place="",
                accio="",
                cofunded=str(item.cofunded or "No"),
                cofunded_ateneu="Sí" if item.cofunded_ateneu else "No",
                strategic_line=(
                    item.strategic_line.name if item.strategic_line else ""
                ),
                admin_url="",
            )
            self.actuacions_obj.add_row(
                group=Actuacions.GROUPS.CREATION.value,
                id=item.pk,
                actuacio_row_obj=row,
                model_obj=item,
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
                material_difusio="No",
                document_acreditatiu="",
                place="",
                accio="",
                cofunded=str(item.cofunded or "No"),
                cofunded_ateneu="Sí" if item.cofunded_ateneu else "No",
                strategic_line=(
                    item.strategic_line.name if item.strategic_line else ""
                ),
                admin_url="",
            )
            self.actuacions_obj.add_row(
                group=Actuacions.GROUPS.CONSOLIDATION.value,
                id=item.pk,
                actuacio_row_obj=row,
                model_obj=item,
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
                material_difusio = "No"
                if item.file1.name:
                    material_difusio = "Sí"
                document_acreditatiu = "No"
                if item.photo2.name:
                    document_acreditatiu = "Sí"
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
                    material_difusio=material_difusio,
                    document_acreditatiu=document_acreditatiu,
                    place=str(item.place) if item.place else "",
                    accio=str(item.course),
                    cofunded=str(item.cofunded or "No"),
                    cofunded_ateneu="Sí" if item.cofunded_ateneu else "No",
                    strategic_line="",
                    admin_url="",
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
                    employment_situation=(
                        participant.get_employment_situation_display() or ""
                    ),
                    birth_place=participant.get_birth_place_display() or "",
                    educational_level=(
                        participant.get_educational_level_display() or ""
                    ),
                    discovered_us=participant.get_discovered_us_display() or "",
                    user_email=participant.email,
                    user_phone_number=participant.phone_number or "",
                    user_project=str(participant.project or ""),
                    user_acompanyaments=(
                        participant.project.stages_list
                        if participant.project
                           and participant.project.stages_list
                        else ""
                    ),
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
                    employment_situation=(
                            participant.get_employment_situation_display() or ""
                    ),
                    birth_place=participant.get_birth_place_display() or "",
                    educational_level=(
                            participant.get_educational_level_display() or ""
                    ),
                    discovered_us=participant.get_discovered_us_display() or "",
                    user_email=participant.email,
                    user_phone_number=participant.phone_number or "",
                    user_project=str(participant.project or ""),
                    user_acompanyaments=(
                        participant.project.stages_list
                        if participant.project
                           and participant.project.stages_list
                        else ""
                    ),
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
                    employment_situation=(
                            participant.get_employment_situation_display() or ""
                    ),
                    birth_place=participant.get_birth_place_display() or "",
                    educational_level=(
                            participant.get_educational_level_display() or ""
                    ),
                    discovered_us=participant.get_discovered_us_display() or "",
                    user_email=participant.email,
                    user_phone_number=participant.phone_number or "",
                    user_project=str(participant.project or ""),
                    user_acompanyaments=(
                        participant.project.stages_list
                        if participant.project
                           and participant.project.stages_list
                        else ""
                    ),
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

    def sheet_insercionslaborals(self):
        self.export_manager.worksheet = self.export_manager.workbook.create_sheet(
            "InsercionsLaborals",
        )
        self.export_manager.row_number = 1
        columns = [
            ("Referència", 20),
            ("Nom actuació", 20),
            ("Cognoms", 20),
            ("Nom", 20),
            ("ID", 20),
            ("Data alta", 20),
            ("Data baixa", 20),
            ("Tipus contracte", 20),
            ("Gènere", 20),
            ("Data naixement", 20),
            ("Població", 20),
            ("NIF Projecte", 20),
            ("Nom projecte", 20),
            ("Cercle / Ateneu (omplir a ma)", 20),
            ("[ convocatòria ]", 20),
        ]
        self.export_manager.create_columns(columns)
        self.fill_insercionslaborals()

    def fill_insercionslaborals(self):
        for insertion in self.insercionslaborals_obj:
            """
            Cada EmploymentInsertion pot anar vinculada a un project o a una
            activity.
            Per poder identificar quina self.actuacions_obj.rows correspon,
            hem de mirar:
              - Si és (GROUPS.CREATION, id),
              - Si és (GROUPS.CONSOLIDATION, id)
              - Si és (GROUPS.ACTIVITY, id)
              - Si és (GROUPS.ACTIVITY_MINORS, id) (tinc dubtes de si mai anirà
                vinculada a una per menors, però com que és possible 
                vincular-les, s'ha de comprovar)
            """
            town = ""
            project_nif = ""
            project_name = ""
            if insertion.project:
                # En el cas d'anar vinculada a un projecte, vol dir que NO sabem a
                # quina ProjectStage correspon.
                # El que farem és agafar el primer ProjectStage VÀLID que trobem,
                # dels que hi hagi per aquesta convocatòria, suposant que n'hi
                # hagi un.
                # "Vàlid" vol dir que tingui sessions, un Estat d'acompanyament
                # correcte, etc. i, per tant, que hagi entrat a
                # self.actuacions_obj.rows.
                #
                # No podem obtenir l'stage fent insertion.project.stages.first()
                # perquè retornarà stages que no són vàlids, a més que
                # comportaria un query extra per cada inserció. En canvi, el que
                # hem fet és que durant el procés d'anar omplint Actuacions.rows
                # s'omple també Actuacions.index_by_project_id, de manera que un
                # cop arribem aquí podem mirar si existeix a l'index i obtenir
                # les dades sense fer més queries:
                project_stage_key = self.actuacions_obj.index_by_project_id.get(
                    insertion.project.id,
                )
                project_stage = self.actuacions_obj.rows.get(project_stage_key)
                if not project_stage:
                    # Significa que han creat una inserció laboral per un
                    # projecte que no té cap acompanyament vàlid.
                    continue
                actuacio_id = project_stage.id
                if insertion.project.town:
                    town = insertion.project.town.name
                project_nif = insertion.project.cif
                project_name = insertion.project.name
            else:
                actuacio_id = insertion.activity.id
                if (
                        insertion.activity.place is not None
                        and insertion.activity.place.town
                ):
                    town = insertion.activity.place.town.name
            # Checking the different possibilities from the most likely to less
            # likely, to optimize performance.
            actuacio_obj = self.actuacions_obj.rows.get(
                (self.actuacions_obj.GROUPS.CREATION.value, actuacio_id)
            ) or self.actuacions_obj.rows.get(
                (self.actuacions_obj.GROUPS.CONSOLIDATION.value, actuacio_id)
            ) or self.actuacions_obj.rows.get(
                (self.actuacions_obj.GROUPS.ACTIVITY.value, actuacio_id)
            ) or self.actuacions_obj.rows.get(
                (self.actuacions_obj.GROUPS.ACTIVITY_MINORS.value, actuacio_id)
            )
            circle = (
                CirclesChoices(insertion.circle).label
                if insertion.circle is not None
                else ""
            )
            row = InsercioLaboralRow(
                actuacio_reference=actuacio_obj.reference,
                user_surname=insertion.user.surname,
                user_name=insertion.user.first_name,
                user_id_number=insertion.user.id_number,
                insercio_data_alta=insertion.insertion_date,
                insercio_data_baixa=insertion.end_date,
                insercio_tipus_contracte=insertion.get_contract_type_display(),
                user_gender=insertion.user.get_gender_display(),
                user_birthdate=insertion.user.birthdate,
                user_town=town,
                project_nif=project_nif,
                project_name=project_name,
                insercio_cercle=circle,
            )
            self.export_manager.fill_row_from_factory(row)

    def sheet_created_projects(self):
        self.export_manager.worksheet = self.export_manager.workbook.create_sheet(
            "EntitatCreada",
        )
        self.export_manager.row_number = 1
        columns = [
            ("Referència", 10),
            ("Nom actuació", 40),
            ("Nom de l'entitat", 40),
            ("NIF de l'entitat", 12),
            ("Nom i cognoms persona de contacte", 30),
            ("Correu electrònic", 12),
            ("Telèfon", 10),
            ("Economia solidària (revisar)", 35),
            ("Ateneu / Cercle", 35),
            ("[Acompanyaments]", 10),
        ]
        self.export_manager.create_columns(columns)
        self.fill_created_projects()

    def fill_created_projects(self):
        """
        By april 2024, created entities are changed. Previously each creation
        had its own row in Actuacions, and then here each CreatedEntity
        was filled in this sheet, calculating its reference number by the
        normal incrementation of the row number and so.
        Now, each creation has to be linked to a ProjectStage, so the rows
        in Actuacions dedicated to CreatedEntity don't exist anymore, and the
        reference number needs to be the corresponding ProjectStage's one.
        """
        for entity_created in self.acompanyaments_creacio:
            if not entity_created.project_stage:
                # Per si de cas algun ateneu no ha fet bé la tasca d'assignar
                # acompanyament a tots els registres de CreatedEntity.
                continue
            actuacio_obj = self.actuacions_obj.rows[
                (
                    self.actuacions_obj.GROUPS.CREATION.value,
                    entity_created.project_stage.id,
                )
            ]
            first_partner = entity_created.project_stage.project.partners.first()
            contact_details = ""
            if first_partner:
                contact_details = first_partner.full_name

            row = CreatedEntityRow(
                actuacio_reference=actuacio_obj.reference,
                project_name=actuacio_obj.row_data.actuacio_name,
                project_nif=entity_created.project_stage.project.cif,
                project_contact_details=contact_details,
                project_email=entity_created.project_stage.project.mail,
                project_phone=entity_created.project_stage.project.phone,
                # Column Economia solidària is hardcoded in CreatedEntityRow
                actuacio_circle=actuacio_obj.row_data.circle,
                project_stages_list=entity_created.project_stage.project.stages_list,
            )
            self.export_manager.fill_row_from_factory(row)

    def sheet_acompanyaments(self):
        self.export_manager.worksheet = self.export_manager.workbook.create_sheet(
            "EntitatCreada",
        )
        self.export_manager.row_number = 1
        columns = [
            ("Referència", 20),
            ("Nom actuació", 40),
            ("Destinatari de l'acompanyament (revisar)", 45),
            ("En cas d'entitat (nom de l'entitat)", 40),
            ("En cas d'entitat (revisar)", 30),
            ("Creació/consolidació", 18),
            ("Data d'inici", 13),
            ("Localitat", 20),
            ("Breu descripció del projecte", 50),
            ("Total hores d'acompanyament", 10),
            ("[Data fi]", 13),
            ("[Docs. justificació]", 10),
        ]
        self.export_manager.create_columns(columns)
        self.fill_acompanyaments()

    def fill_acompanyaments(self):
        for project_stage in self.acompanyaments_consolidacio:
            actuacio_obj = self.actuacions_obj.rows[
                (
                    self.actuacions_obj.GROUPS.CONSOLIDATION.value,
                    project_stage.id,
                )
            ]
            start_date = (
                project_stage.earliest_session.date if project_stage.earliest_session
                else ""
            )
            project_description = ""
            if project_stage.project.description:
                # Fa falta l'IF pq per error Project.descripcion és nullable
                project_description = project_stage.project.description
            latest_session_date = (
                project_stage.latest_session.date if project_stage.latest_session
                else ""
            )

            row = AcompanyamentRow(
                actuacio_reference=actuacio_obj.reference,
                # Column Entitat: hardcoded
                project_name=actuacio_obj.row_data.actuacio_name,
                project_status=project_stage.project.get_project_status_display(),
                stage_type=project_stage.get_stage_type_display(),
                start_date=start_date,
                town=actuacio_obj.row_data.circle,
                short_description=project_description,
                total_hours=project_stage.hours_sum(),
                latest_session_date=latest_session_date,
                justification_documents_total=project_stage.justification_documents_total,
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
    obj: object = None

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
        self.index_by_project_id = {}

    def get_row(self, group, id):
        pass

    def add_row(self, group, id, actuacio_row_obj, model_obj=None):
        """
        :param group: one of self.GROUPS
        :param id: The row's item database ID
        :param actuacio_row_obj: An ActuacioRow instance
        :param model_obj: An instance of ProjectStage or Activity
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
            obj=model_obj,
        )
        self.rows[(group, id)] = actuacio_obj

        project_groups = (
            self.GROUPS.CREATION,
            self.GROUPS.CONSOLIDATION,
        )
        if model_obj and group in project_groups:
            self.index_by_project_id.update(
                {model_obj.project.id: (group, id)}
            )

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
