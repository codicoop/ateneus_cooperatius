from django.db.models import Q

from apps.cc_courses.choices import ProjectStageStatesChoices
from apps.coopolis.choices import CirclesChoices, SubServicesChoices
from apps.coopolis.models import ProjectStage, Project, EmploymentInsertion
from apps.cc_courses.models import Activity
from apps.coopolis.models.projects import CreatedEntity
from apps.dataexports.exports.manager import ExcelExportManager


class ExportJustificationService:
    # This value is specified whenever we call get_formatted_reference. This
    # property here is only a fallback, used when it's not passed to
    # get_formatted_reference. In future refactors can be deleted and make the
    # parameter in get_formatted_reference required.
    subsidy_period_str = "2021-22"

    def __init__(self, export_obj):
        self.export_manager = ExcelExportManager(
            export_obj,
            correlations_fixtures_filename="correlations_2021_2022.json",
        )
        self.number_of_activities = 0
        self.number_of_stages = 0
        self.number_of_nouniversitaris = 0
        self.number_of_founded_projects = 0
        # A 2021-22 decidim que exportem els projectes per duplicat en cas que
        # hi hagi un itinerari de creació i un de consolidació.
        # Per agrupar-ho en un sol itinerari, ho teníem així:
        #             9: 'creacio',  # Incubació
        #             11: 'creacio',  # Creació
        #             12: 'creacio',  # Consolidació
        #
        # El que fa aquest dict és indicar quin nom tindrà cada ID de tipus
        # d'acompanyament, per quan arriba el moment en que agafem les dades i
        # generem el self.stages_obj, aquest nom es farà servir com a clau del
        # diccionari.
        # Per tant, si a tots els tipus d'acompanyament els hi posem la mateixa
        # key, a l'excel tindrem una sola fila amb la suma de totes les hores.
        # Però si cada un té una key diferent, apareixerà tantes vegades com
        # tipus d'acompanyament hi hagi.
        self.stages_groups = {
            9: 'incubacio',  # Era Incubació
            11: 'creacio',  # Creació
            12: 'consolidacio',  # Consolidació
        }
        self.stages_obj = None
        self.sessions_obj = None

    def get_sessions_obj(self, for_minors=False):
        return Activity.objects.filter(
            Q(
                date_start__range=self.export_manager.subsidy_period.range,
                for_minors=for_minors
            ) & (
                Q(cofunded__isnull=True) | (
                    Q(cofunded__isnull=False) & Q(cofunded_ateneu=True)
                )
            )
        )
    
    """
    
    Exportació Ateneu
    
    """
    def export(self):
        """ Each function here called handles the creation of one of the
        worksheets."""
        self.export_actuacions()
        self.export_participants()
        self.export_nouniversitaris()
        self.export_insercionslaborals()
        self.export_founded_projects()
        self.export_stages()

        return self.export_manager.return_document("justificacio")

    def export_actuacions(self):
        # Tutorial: https://djangotricks.blogspot.com/2019/02/how-to-export-
        # data-to-xlsx-files.html
        # Docs: https://openpyxl.readthedocs.io/en/stable/
        # tutorial.html#create-a-workbook
        self.export_manager.worksheet.title = "Actuacions"

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
        ]
        self.export_manager.create_columns(columns)
        self.actuacions_rows_activities()
        self.actuacions_rows_stages()
        self.actuacions_rows_nouniversitaris()
        # Abans hi havia un últim bloc on apareixien els projectes creats
        # a banda. S'ha canviat de manera que els projectes creats han d'anar
        # vinculats a un acompanyament i, per tant, els projectes creats
        # apareixeran enmig del bloc actuacions_rows_stages.
        # Total Stages: self.export_manager.row_number-Total Activities-1

    def actuacions_rows_activities(self):
        self.sessions_obj = self.get_sessions_obj()
        self.number_of_activities = len(self.sessions_obj)
        for item in self.sessions_obj:
            self.export_manager.row_number += 1

            service = (
                item.get_service_display()
                if item.service
                else ("", True)
            )
            sub_service = (
                item.get_sub_service_display()
                if item.sub_service
                else ("", True)
            )
            town = ("", True)
            if item.place is not None and item.place.town:
                town = self.export_manager.get_correlation("towns", item.place.town.name)
            material_difusio = "No"
            if item.file1.name:
                material_difusio = "Sí"
            document_acreditatiu = "No"
            if item.photo2.name:
                document_acreditatiu = "Sí"
            circle = (
                 CirclesChoices(item.circle).label
                 if item.circle is not None
                 else ("", True)
            )

            row = [
                service,
                sub_service,
                item.name,
                item.date_start,
                "",
                str(item.entity) if item.entity else '',  # Entitat
                circle,
                town,
                item.enrolled.count(),
                material_difusio,
                document_acreditatiu,
                "",
                str(item.place) if item.place else '',  # Lloc
                str(item.course),  # Acció
                str(item.cofunded or "No"),  # Cofinançat
                "Sí" if item.cofunded_ateneu else "No",  # Cofinançat amb AACC
                item.get_circle_display(),
            ]
            self.export_manager.fill_row_data(row)

    def get_stages_obj(self):
        return ProjectStage.objects.order_by('date_start').filter(
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

    def actuacions_rows_stages(self):
        """
        Acompanyaments que han d'aparèixer:
        - Tots els que siguin tipus Creació o Consolidació.
        - Idem però pels acompanyaments d'Incubació.
        - Sempre que ProjectStage.stage_state NO sigui
          ProjectStageStatesChoices.PENDING
        Per tant com a màxim apareixerà 2 vegades.

        A banda hi ha l'exportació en 2 itineraris, on s'hi separaran els de
        Creació i els de Consolidació.
        """
        obj = self.get_stages_obj()
        self.stages_obj = {}
        for item in obj:
            if int(item.stage_type) not in self.stages_groups:
                continue
            group = self.stages_groups[int(item.stage_type)]
            p_id = item.project.id
            if p_id not in self.stages_obj:
                self.stages_obj.update({
                    p_id: {}
                })
            if group not in self.stages_obj[p_id]:
                self.stages_obj[p_id].update({
                    group: {
                        'obj': item,
                        'total_hours': 0,
                        'participants': []
                    }
                })
            self.stages_obj[p_id][group]['total_hours'] += item.hours_sum()

            # Aprofitem per omplir les dades dels participants aquí per no
            # repetir el procés més endavant. La qüestió és que encara que un
            # participant hagi participat a diversos acompanyaments, aquí
            # només aparegui una vegada.
            for participant in item.partners_involved_in_sessions:
                if (
                    participant
                    not in self.stages_obj[p_id][group]['participants']
                ):
                    self.stages_obj[p_id][group]['participants'].append(
                        participant
                    )
        """
        En aquest punt, self.stages_obj té aquesta estructura:
        160: {
            'nova_creacio': {
                'obj': '<ProjectStage: Consell Comarcal Conca de Barberà - Concactiva: 00 Nova creació - acollida>',
                'total_hours': 3,
                'participants': [
                         '<User: Jordi París>', '<User: Francesc Viñas>',
                         '<User: Carme Pallàs>',
                         '<User: Pere Picornell Busquets>'
                ],
                'row_number': 122
            }
        },
        20: {
            'consolidacio': {
                'obj': '<ProjectStage: La Providència SCCL: 04 Consolidació - acompanyament>',
                'total_hours': 36,
                'participants': [
                    '<User: Teresa Trilla Ferré>',
                    '<User: Marc Trilla Güell>',
                    '<User: Gerard Nogués Balsells>',
                    '<User: tais bastida aubareda>'
                ],
                'row_number': 126},
            'nova_creacio': {
                'obj': '<ProjectStage: La Providència SCCL: 02 Nova creació - constitució>',
                'total_hours': 7,
                'participants': [
                    '<User: Marc Trilla Güell>',
                    '<User: Esther Perello Piulats>'
                ],
                'row_number': 127
            }
        }, 
        
        És a dir, cada Projecte té un element amb la seva ID, que conté els
        grups que corresponguin.
        Cada grup conté:
            - Una instància de l'objecte ProjectStage (el primer que hagi pillat)
            - 'total_hours', amb la suma de totes les hores de tots els ProjectStages
                del mateix grup i projecte.

        A continuació el que farem és afegir com a row cada un d'aquests grups.
        De manera que cada itinerari (creació, consolidació..) de cada projecte
        tindrà la seva propia fila a Actuacions.
        
        En el procés de fer-ho, aprofitem per desar el nº de row dins 
        self.stages_obj[id_projecte][nom_grup][row_number]
        per poder-ho fer servir més endavant quan generem els rows de les 
        persones participants.
        """

        self.number_of_stages = 0
        for project_id, project in self.stages_obj.items():
            for group_name, group in project.items():
                self.number_of_stages += 1
                item = group['obj']
                self.export_manager.row_number += 1

                # Desant el nº per quan fem el llistat de participants. El
                # self.export_manager.row_number conté el row REAL, que com que inclou la fila
                # de headers, és un més que la que s'assignarà com a
                # referència.
                self.stages_obj[project_id][group_name][
                    'row_number'
                ] = self.export_manager.row_number - 1

                service = (
                    item.get_service_display()
                    if item.service
                    else ("", True)
                )
                sub_service = (
                    item.get_sub_service_display()
                    if item.sub_service
                    else ("", True)
                )
                town = ("", True)
                if item.project.town:
                    town = self.export_manager.get_correlation(
                        "towns", item.project.town.name,
                    )
                circle = (
                     CirclesChoices(item.circle).label
                     if item.circle is not None
                     else ("", True)
                )

                row = [
                    service,
                    sub_service,  # Subservei, pendent.
                    item.project.name,
                    item.date_start if not None else '',
                    "",
                    item.entities_str,  # Entitat/s
                    circle,
                    town,
                    len(group['participants']),  # Nombre de participants
                    "No",
                    "",
                    "",  # Incidències
                    '(no aplicable)',  # Lloc
                    '(no aplicable)',  # Acció
                    str(item.cofunded or "No"),  # Cofinançat
                    "Sí" if item.cofunded_ateneu else "No",  # Cofinançat amb AACC
                    item.get_circle_display(),
                ]
                self.export_manager.fill_row_data(row)

    def actuacions_rows_nouniversitaris(self):
        obj = self.get_sessions_obj(for_minors=True)
        self.number_of_nouniversitaris = len(obj)
        for item in obj:
            self.export_manager.row_number += 1

            service = (
                item.get_service_display()
                if item.service
                else ("", True)
            )
            sub_service = (
                item.get_sub_service_display()
                if item.sub_service
                else ("", True)
            )
            town = ("", True)
            if item.place and item.place.town:
                town = self.export_manager.get_correlation(
                    "towns", item.place.town.name,
                )
            material_difusio = "No"
            if item.file1.name:
                material_difusio = "Sí"
            document_acreditatiu = "No"
            if item.photo2.name:
                document_acreditatiu = "Sí"
            circle = (
                 CirclesChoices(item.circle).label
                 if item.circle is not None
                 else ("", True)
            )

            row = [
                service,
                sub_service,
                item.name,
                item.date_start,
                "",
                str(item.entity) if item.entity else '',  # Entitat
                circle,
                town,
                item.minors_participants_number,
                material_difusio,
                document_acreditatiu,
                "",
                str(item.place) if item.place else '',  # Lloc
                str(item.course),  # Acció
                str(item.cofunded or "No"),  # Cofinançat
                "Sí" if item.cofunded_ateneu else "No",  # Cofinançat amb AACC
                item.get_circle_display(),
            ]
            self.export_manager.fill_row_data(row)

    def export_stages(self):
        self.export_manager.worksheet = self.export_manager.workbook.create_sheet(
            "Acompanyaments")
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

        self.stages_rows()

    def stages_rows(self):
        reference_number = self.number_of_activities

        for p_id, stage in self.stages_obj.items():
            for group_name, group in stage.items():
                self.export_manager.row_number += 1
                reference_number += 1
                item = group['obj']

                hours = group['total_hours']
                town = ("", True)
                if item.project.town:
                    town = self.export_manager.get_correlation(
                        "towns", item.project.town.name,
                    )
                crea_consolida = self.export_manager.get_correlation(
                    "stage_type",
                    item.stage_type,
                )

                row = [
                    self.get_formatted_reference(
                        reference_number,
                        item.sub_service,
                        item.entities_str,
                        item.circle,
                    ),
                    item.project.name,
                    # Camp no editable, l'ha d'omplir l'excel automàticament.
                    "Entitat",
                    # "Destinatari de l'actuació" Opcions: Persona física/Promotor del projecte/Entitat PENDENT.
                    item.project.name,  # "En cas d'entitat (Nom de l'entitat)"
                    self.export_manager.get_correlation(
                        "project_status", item.project.project_status),
                    crea_consolida or ("", True),
                    # "Creació/consolidació".
                    item.date_start or ("", True),
                    town,
                    item.project.description or ("", True),  # Breu descripció.
                    hours or ("0", True),  # Total hores d'acompanyament.
                    item.latest_session.date if item.latest_session else '',
                    item.justification_documents_total,
                ]
                self.export_manager.fill_row_data(row)

    def export_founded_projects(self):
        self.export_manager.worksheet = \
            self.export_manager.workbook.create_sheet("EntitatCreada")
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

        self.founded_projects_rows()

    def founded_projects_rows(self):
        """
        By april 2024, created entities are changed. Previously each creation
        had its own row in Actuacions, and then here each CreatedEntity
        was filled in this sheet, calculating its reference number by the
        normal incrementation of the row number and so.
        Now, each creation has to be linked to a ProjectStage, so the rows
        in Actuacions dedicated to CreatedEntity don't exist anymore, and the
        reference number needs to be the corresponding ProjectStage's one.

        When ProjectStages rows are rendered, we're creating a dictionary
        with all the information that includes the row number.
        We're using that here, by doing:
        1. Loop through all self.stages_obj
        2. For each ProjectStage, check if there's a CreatedEntity registry.
        3. If so, create the row, and calculate the reference number using
        this stages_obj stored row number.
        """

        self.export_manager.row_number += 1
        for project_id, project in self.stages_obj.items():
            for group_name, group in project.items():
                stage = group['obj']
                if not hasattr(stage, "created_entity"):
                    continue
                stage_reference_number = group['row_number']
                created_entity = stage.created_entity
                circle = (
                    CirclesChoices(created_entity.circle).label
                    if created_entity.circle else ("", True)
                )
                contact_details = (
                    created_entity.project.partners.all()[0].full_name
                    if created_entity.project.partners.all() else ("", True)
                )
                row = [
                    self.get_formatted_reference(
                        stage_reference_number,
                        created_entity.sub_service,
                        created_entity.entity,
                        created_entity.circle,
                    ),  # Referència
                    "",  # Nom actuació
                    created_entity.project.name,  # Nom del projecte
                    created_entity.project.cif or ("", True),  # NIF del projecte
                    contact_details,  # Nom i cognoms persona de contacte
                    created_entity.project.mail or ("", True),  # Correu electrònic
                    created_entity.project.phone or ("", True),  # Telèfon
                    "Sí",  # Economia solidària
                    circle,  # Ateneu / Cercle
                    created_entity.project.stages_list,  # Acompanyaments
                ]
                self.export_manager.fill_row_data(row)

    def export_participants(self):
        self.export_manager.worksheet = \
            self.export_manager.workbook.create_sheet("Participants")
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

        self.participants_rows()
        self.participants_project_stages_rows()

    def participants_project_stages_rows(self):
        for project_id, project in self.stages_obj.items():
            for group_name, group in project.items():
                stage = group['obj']
                stage_reference_number = group['row_number']
                for participant in group['participants']:
                    gender = ("", True)
                    if participant.gender:
                        gender = self.export_manager.get_correlation(
                            'gender',
                            participant.gender,
                        )
                    town = ("", True)
                    if participant.town:
                        town = self.export_manager.get_correlation(
                            "towns", participant.town.name,
                        )

                    row = [
                        self.get_formatted_reference(
                            stage_reference_number,
                            stage.sub_service,
                            stage.entities_str,
                            stage.circle,
                        ),
                        stage.project.name,
                        # Nom de l'actuació. Camp automàtic de l'excel.
                        participant.surname or "",
                        participant.first_name,
                        participant.id_number or ("", True),
                        gender,
                        participant.birthdate or ("", True),
                        town,
                        participant.get_employment_situation_display() or "",
                        participant.get_birth_place_display() or "",
                        participant.get_educational_level_display() or "",
                        participant.get_discovered_us_display() or "",
                        participant.email,
                        participant.phone_number or "",
                        str(participant.project) or "",
                        participant.project.stages_list if participant.project and participant.project.stages_list else "",
                    ]
                    self.export_manager.row_number += 1
                    self.export_manager.fill_row_data(row)

    def participants_rows(self):
        activity_reference_number = 0
        obj = self.get_sessions_obj(for_minors=False)
        for activity in obj:
            # We know that activities where generated first, so it starts at 1.
            activity_reference_number += 1
            for enrollment in activity.confirmed_enrollments:
                participant = enrollment.user
                self.export_manager.row_number += 1
                if participant.gender is None:
                    gender = ("", True)
                else:
                    gender = self.export_manager.get_correlation(
                        'gender', participant.gender)
                town = ("", True)
                if participant.town:
                    town = self.export_manager.get_correlation(
                        "towns", participant.town.name,
                    )

                row = [
                    self.get_formatted_reference(
                        activity_reference_number,
                        activity.sub_service,
                        activity.entity,
                        activity.circle,
                    ),
                    activity.name,
                    # Nom de l'actuació. Camp automàtic de l'excel.
                    participant.surname or ("", True),
                    participant.first_name,
                    participant.id_number,
                    gender,
                    participant.birthdate or ("", True),
                    town,
                    participant.get_employment_situation_display() or "",
                    participant.get_birth_place_display() or "",
                    participant.get_educational_level_display() or "",
                    participant.get_discovered_us_display() or "",
                    participant.email,
                    participant.phone_number or "",
                    str(participant.project) if participant.project else "",
                    participant.project.stages_list if participant.project and participant.project.stages_list else "",
                ]
                self.export_manager.fill_row_data(row)

    def export_nouniversitaris(self):
        self.export_manager.worksheet = \
            self.export_manager.workbook.create_sheet(
                "ParticipantsNoUniversitaris"
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

        self.nouniversitaris_rows()

    def nouniversitaris_rows(self):
        nouniversitari_reference_number = \
            self.number_of_stages \
            + self.number_of_activities
        obj = self.get_sessions_obj(for_minors=True)
        for activity in obj:
            self.export_manager.row_number += 1
            nouniversitari_reference_number += 1
            row = [
                self.get_formatted_reference(
                    nouniversitari_reference_number,
                    activity.sub_service,
                    activity.entity,
                    activity.circle,
                ),
                activity.name,  # Nom de l'actuació. Camp automàtic de l'excel.
                self.export_manager.get_correlation(
                    'minors_grade', activity.minors_grade),
                activity.minors_school_name,
                activity.minors_participants_number,
            ]
            self.export_manager.fill_row_data(row)

    def export_insercionslaborals(self):
        self.export_manager.worksheet = \
            self.export_manager.workbook.create_sheet("InsercionsLaborals")
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

        self.insercionslaborals_rows()

    def insercionslaborals_rows(self):
        obj = EmploymentInsertion.objects.filter(
            subsidy_period__date_start__range=self.export_manager.subsidy_period_range)
        for insertion in obj:
            self.export_manager.row_number += 1
            id_number = insertion.user.id_number
            if not id_number:
                id_number = ('', True)
            insertion_date = insertion.insertion_date
            if not insertion_date:
                insertion_date = ('', True)
            contract_type = insertion.get_contract_type_display()
            if not contract_type:
                contract_type = ('', True)
            birthdate = insertion.user.birthdate
            if not birthdate:
                birthdate = ('', True)
            town = ('', True)
            if insertion.user.town:
                town = self.export_manager.get_correlation(
                    "towns", insertion.user.town.name,
                )
            if insertion.user.gender is None:
                gender = ""
            else:
                gender = self.export_manager.get_correlation(
                    'gender', insertion.user.gender)
            circle = (
                 CirclesChoices(insertion.circle).label
                 if insertion.circle is not None
                 else ""
            )
            cif = ('', True)
            name = ('', True)
            reference = ("", True)
            if insertion.project:
                if insertion.project.cif:
                    cif = insertion.project.cif
                name = insertion.project.name
                project = self.stages_obj.get(insertion.project.id)
                reference = self.get_formatted_reference_for_project(project)
            if insertion.activity:
                reference = self.get_formatted_reference_for_activity(
                    insertion.activity,
                )

            row = [
                reference,  # Deixem referència en blanc pq la posin a ma.
                '',  # Nom actuació
                insertion.user.surname,
                insertion.user.first_name,  # Persona
                id_number,
                insertion_date,  # Data d'alta SS
                insertion.end_date or "",  # Data baixa SS
                contract_type,  # Tipus de contracte
                gender,
                birthdate,
                town,
                cif,
                name,  # Projecte
                circle,  # Cercle / Ateneu
                str(insertion.subsidy_period),  # Convocatòria
            ]
            self.export_manager.fill_row_data(row)

    def get_formatted_reference_for_activity(self, activity):
        activity_row_number = 0
        for loaded_activity in self.sessions_obj:
            activity_row_number += 1
            if loaded_activity.id == activity.id:
                print("trobada")
                break
            # Using 0 as a flag for "did not match any activity"
            activity_row_number = 0

        if not activity_row_number or not activity.entity:
            return "", True

        reference = self.get_formatted_reference(
            activity_row_number,
            activity.sub_service,
            str(activity.entity),
            activity.circle,
        )
        return reference

    def get_formatted_reference_for_project(self, project):
        reference = ("", True)
        """
        Project en principì ha de contenir almenys un element que serà un
        diccionari amb les dades de l'acompanyament.
        En pot contenir diversos, i en volem agafar un d'ells, el que sigui,
        així que iterem el diccionari 1 vegada per obtenir el primer.

        Això és un exemple del que pot contenir, tenint en compte que 
        no podem saber segur el nom de la clau del o dels diccionaris.
        'consolidacio': {
            'obj': '<ProjectStage: La Providència SCCL: 04 Consolidació - acompanyament>',
            'total_hours': 36,
            'participants': [
                '<User: Teresa Trilla Ferré>',
                '<User: Marc Trilla Güell>',
                '<User: Gerard Nogués Balsells>',
                '<User: tais bastida aubareda>'
            ],
            'row_number': 126},
        'nova_creacio': {
            'obj': '<ProjectStage: La Providència SCCL: 02 Nova creació - constitució>',
            'total_hours': 7,
            'participants': [
                '<User: Marc Trilla Güell>',
                '<User: Esther Perello Piulats>'
            ],
            'row_number': 127
        }
        """
        if project:
            stage = next(iter(project.values()))
            reference = self.get_formatted_reference(
                stage["row_number"],
                stage["obj"].sub_service,
                stage["obj"].entities_str,
                stage["obj"].circle,
            )
        return reference

    def export_all_projects(self):
        self.export_manager.worksheet = self.export_manager.workbook.create_sheet(
            "PROJECTES",
        )
        self.export_manager.row_number = 1

        columns = [
            ("ID", 5),
            ("Data registre", 12),
            ("Data constitució", 12),
            ("Nom de l'entitat", 40),
            ("NIF de l'entitat", 12),
            ("Nom i cognoms persona de contacte", 30),
            ("Correu electrònic", 30),
            ("Telèfon", 15),
            ("[Acompanyaments]", 40),
            ("[Serveis]", 40),
        ]
        self.export_manager.create_columns(columns)

        self.all_projects_rows()

    def all_projects_rows(self):
        self.export_manager.row_number = 1
        obj = Project.objects.order_by('id').all()
        for project in obj:
            self.export_manager.row_number += 1
            row = [
                project.id,
                project.registration_date if project.registration_date else "",
                project.constitution_date if project.constitution_date else "",
                project.name,
                project.cif if project.cif else "",
                project.partners.all()[
                    0].full_name if project.partners.all() else "",
                project.mail,
                project.phone,
                project.stages_list if project.stages_list else "",
                project.services_list if project.services_list else ""
            ]
            self.export_manager.fill_row_data(row)

    def get_formatted_reference(
        self,
        ref_num,
        sub_service_id,
        entity,
        circle_id,
        subsidy_period=None,
    ):
        if not sub_service_id or circle_id is None or not entity:
            return "", True
        if not subsidy_period:
            subsidy_period = self.subsidy_period_str
        sub_service = SubServicesChoices(sub_service_id).label
        circle = CirclesChoices(circle_id).label
        return (
            f"{ref_num} - {sub_service} {subsidy_period} {entity} - {circle}"
        )
