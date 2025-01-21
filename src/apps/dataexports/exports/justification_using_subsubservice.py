from dataclasses import dataclass

from django.db.models import Q

from apps.cc_courses.choices import ProjectStageStatesChoices, StageTypeChoices
from apps.coopolis.models import ProjectStage, EmploymentInsertion
from apps.cc_courses.models import Activity
from apps.coopolis.models.projects import CreatedEntity
from apps.dataexports.exports.manager import ExcelExportManager
from apps.dataexports.exports.row_factories import BaseRow


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

        """
        Fins aquí la idea és anar desant els querysets dels rows de totes les
        sheets.
        OJO: pendent d"afegir allò de que agafi les dades relacionades quan fa
        el query inicial.
        Segurament serà la cosa que accelerarà més el procés.
        select_related, prefetch_related
        
        
        D"aquestes dades, algunes han d"anar a Actuacions, i necessitem desar
        el nº de row + el número de referència + la (ID item + tipus item) -per
        poder-lo localitzar després-.
        
        Les que van a Actuacions son:
        - Sessions
        - Entitats creades (és a dir, l"acompanyament que tingui vinculat)
        - Acompanyaments consolidació
        - Acompanyaments incubació
        
        Llavors farem un bucle per cada un d"aquests 4 objs i en un altre objecte,
        tipus ActuacionsRows, per cada un dels items hi guardem les dades
        que deia abans:
        - Número de row
        - Referència
        - ID item
        - Group (Tipus item)
        - row_data - Cada una de les dades d"Actuacions (AIXÒ PODRIEN SER OBJECTES ActuacioRow):
            - Servei
            - Subservei
            - Nom de l"actuació
            - Data inici d"actuació
            - Període d"actuacions
            - Entitat que realitza l"actuació
            - Cercle / Ateneu
            - Municipi
            - Nombre de participants
            - Material de difusió (S/N)
        - El propi objecte???
        
        ActuacionsRows necessitarà tenir una cosa tipus
        ActuacionsRows.get_session(id)
        ActuacionsRows.get_acompanyament_consolidacio(id)
        ActuacionsRows.get_acompanyament_incubació(id)
        ActuacionsRows.get_acompanyament_creacio(id)
        
        I llavors o bé fer un bucle, o millor, que intenti buscar només per la ID,
        i en cas que obtingui més d"un resultat, que faci un bucle pels obtinguts.
        Així tots els que amb ActuacionsRows[12345] ja siguin el bo (la majoria
        sinó tots) s"estalviaran qualsevol bucle.
        O bé, que la KEY ja sigui un prefix+númeroID, tipus
        session12345
        consolidacio123345
        I aquestes funcions s"ocupin de retornar.
        MILLOR AIXÍ MÉS FÀCIL I EFICIENT.
        
        Llavors aniria bé tenir una funció set_csession, 
        set_acompanyament_consolidacio, etc. que s"encarregui de desar la dada
        amb la ID ben posada.
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


class Sessions:
    """
    Idea:
    Tenir Sessions i ProjectStages, que seran classes que contindran un
    diccionari o llista amb tots els items corresponents, però processats,
    de manera que cada item contingui:
    - El número de row absolut a la sheet Actuacions
    - El número de referència
    - Tots els camps que necessitem tant per la sheet Actuacions com per les
      altres sheets a on aparegui.
    - Un índex o key o manera de localitzar un item concret.
    - Una manera d"obtenir-los tots ordenats pel número de row.

    Fet això, omplir Actuacions i Projectes acompanyats és fàcil, tot i que
    ajudaria tenir una altra classe a on li posem una llista de tots els
    items de la sheet, és a dir els rows?
    Ho dic pq Actuacions mostra rows amb items de tots dos objectes.
    Però potser no cal i a la funció on els renderitzem, els posem uns
    darrera dels altres.

    Però què passa amb Insercions Laborals, Participants, Entitats Creades...?

    Participants: actualment fem un bucle que passi per tots els obj de les
    activitats, i per cada una fer un for per activity.confirmed_enrollments,
    i de cada enrollment, en fem una row.
    Ens serviria de la mateixa manera, mentre incloguem els confirmed_enrollments
    a cada item de Session.items.
    Al fer aquest foreach, pot omplir una llista d"objectes ParticipantRow.

    Després fem:
        for row in rows:
            self.export_manager.fill_row_from_factory(row)

    Insercions laborals, Entitats creades, Per menors: seria el mateix que lo
    anterior.
    És a dir enfocat així, cada sheet farà un bucle per les dades que realment
    toquen allà, i disposarà de Session i de ProjectStages per consultar-hi
    el registre que necessitin a cada moment, i així tenir el número de referència
    i les dades que puguin necessitar d"allà.

    """
    pass


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
class Actuacio:
    row_number: str
    reference: str
    id: str
    group: str
    row_data: str


class Actuacions:
    last_row = 0
    rows = {}
    GROUPS = [
        "session",
        "consolidacio",
        "incubacio",
        "creacio",
    ]

    def validate_group(self, group):
        if not group in self.GROUPS:
            raise ValueError(
                f"Group {group} should be one of: {', '.join(self.GROUPS)}"
            )

    def get_row(self, group, id):
        self.validate_group(group)

    def add_row(self, group, id, actuacio_row_obj):
        """
        :param group: one of self.GROUPS
        :param id: The row's item database ID
        :param actuacio_row_obj: An ActuacioRow instance
        :return: Nothing
        """
        self.validate_group(group)
        """
        La funció haurà de fer:
        - Validar el grup
        - Comprovar que l'id no existeixi ja
        - Afegir la nova fila a la llista de rows
        - Generar nou número de row amb self.last_row += 1
        - Generar la referència (falta copiar la funció per generar referències).
          Ojo faran falta les dades de actuacio_row_obj.
        - Omplir un nou objecte Actuacio amb les dades, incloent actuacio_row_obj
        - Afegir-lo a self.rows[(group, id)]
        
        Dades:
        - Número de row
        - Referència
        - ID item
        - Group (Tipus item)
        - row_data - Cada una de les dades d"Actuacions (AIXÒ PODRIEN SER OBJECTES ActuacioRow):
            - Servei
            - Subservei
            - Nom de l"actuació
            - Data inici d"actuació
            - Període d"actuacions
            - Entitat que realitza l"actuació
            - Cercle / Ateneu
            - Municipi
            - Nombre de participants
            - Material de difusió (S/N)
        - El propi objecte??? millor no, per no acoplar tant
        """
