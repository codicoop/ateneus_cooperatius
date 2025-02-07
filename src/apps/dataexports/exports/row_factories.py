from dataclasses import dataclass
from typing import Union


class BaseRow:
    def get_columns(self) -> list:
        return []

    def get_format_method(self):
        return None


class GlobalReportYesNoEmptyRow(BaseRow):
    def __init__(
        self,
        title: str,
        cap: tuple = (),
        ateneu: tuple = (),
        cercle1: tuple = (),
        cercle2: tuple = (),
        cercle3: tuple = (),
        cercle4: tuple = (),
        cercle5: tuple = (),
    ):
        self.title = title
        self.cap = self.to_yes_no_empty(cap)
        self.ateneu = self.to_yes_no_empty(ateneu)
        self.cercle1 = self.to_yes_no_empty(cercle1)
        self.cercle2 = self.to_yes_no_empty(cercle2)
        self.cercle3 = self.to_yes_no_empty(cercle3)
        self.cercle4 = self.to_yes_no_empty(cercle4)
        self.cercle5 = self.to_yes_no_empty(cercle5)

    def to_yes_no_empty(self, values):
        if len(values) == 3:
            if (
                values[0] is None
                or values[1] is None
                or values[2] is None
            ):
                return "Sense dades"
            return f"Sí {values[0]}, No {values[1]}, Blanc {values[2]}"
        return "-"

    def get_columns(self) -> list:
        return [
            self.title,
            self.cap,
            self.ateneu,
            self.cercle1,
            self.cercle2,
            self.cercle3,
            self.cercle4,
            self.cercle5,
        ]


class GlobalReportRow(BaseRow):
    value_if_empty = "-"

    def __init__(
        self,
        title: str,
        cap: int = 0,
        ateneu: int = 0,
        cercle1: int = 0,
        cercle2: int = 0,
        cercle3: int = 0,
        cercle4: int = 0,
        cercle5: int = 0,
        values_dict: dict = None,
        values_dict_field: str = None,
    ):
        self.title = title
        self.cap = cap
        self.ateneu = ateneu
        self.cercle1 = cercle1
        self.cercle2 = cercle2
        self.cercle3 = cercle3
        self.cercle4 = cercle4
        self.cercle5 = cercle5
        if values_dict and values_dict_field:
            self.cap = values_dict["cap"].get(values_dict_field)
            self.ateneu = values_dict["ateneu"].get(values_dict_field)
            self.cercle1 = values_dict["cercle1"].get(values_dict_field)
            self.cercle2 = values_dict["cercle2"].get(values_dict_field)
            self.cercle3 = values_dict["cercle3"].get(values_dict_field)
            self.cercle4 = values_dict["cercle4"].get(values_dict_field)
            self.cercle5 = values_dict["cercle5"].get(values_dict_field)

    def get_columns(self) -> list:
        return [
            self.title,
            round(self.cap, 1) if self.cap else self.value_if_empty,
            round(self.ateneu, 1) if self.ateneu else self.value_if_empty,
            round(self.cercle1, 1) if self.cercle1 else self.value_if_empty,
            round(self.cercle2, 1) if self.cercle2 else self.value_if_empty,
            round(self.cercle3, 1) if self.cercle3 else self.value_if_empty,
            round(self.cercle4, 1) if self.cercle4 else self.value_if_empty,
            round(self.cercle5, 1) if self.cercle5 else self.value_if_empty,
        ]


class EmptyRow(BaseRow):
    pass


class MultiTextColRow(BaseRow):
    def __init__(self, values: list):
        self.values = values
        for value in self.values:
            if type(value) is not str:
                raise TypeError(f"{value} is not a string.")

    def get_columns(self) -> list:
        return self.values


class TextRow(BaseRow):
    def __init__(self, title: str):
        self.title = title

    def get_columns(self) -> list:
        return [self.title, ]


class TitleRow(TextRow):
    def get_format_method(self) -> tuple:
        return "format_cell_bold", 1


class TextWithValue(BaseRow):
    def __init__(self, title: str, value: Union[int, str] = 0):
        self.title = title
        self.value = value

    def get_columns(self) -> list:
        return [
            self.title,
            round(self.value, 1) if type(self.value) is float else self.value
        ]


class TextWithYesNoEmpty(BaseRow):
    def __init__(self, title: str, values: tuple = ()):
        self.title = title
        self.value = self.to_yes_no_empty(values)

    def to_yes_no_empty(self, values):
        if len(values) == 3:
            if (
                    values[0] is None
                    or values[1] is None
                    or values[2] is None
            ):
                return "Sense dades"
            return f"Sí {values[0]}, No {values[1]}, Blanc {values[2]}"
        return "-"

    def get_columns(self) -> list:
        return [self.title, self.value]


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
    material_difusio: str
    document_acreditatiu: str
    place: str
    accio: str  # Course
    cofunded: str
    cofunded_ateneu: str
    strategic_line: str
    admin_url: str
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
            self.material_difusio or self.value_if_empty,
            self.document_acreditatiu or self.value_if_empty,
            self.place or self.value_if_empty,
            self.accio or self.value_if_empty,
            self.cofunded or self.value_if_empty,
            self.cofunded_ateneu or self.value_if_empty,
            self.strategic_line or self.value_if_empty,
            self.admin_url or self.value_if_empty,
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
    employment_situation: str
    birth_place: str
    educational_level: str
    discovered_us: str
    user_email: str
    user_phone_number: str
    user_project: str
    user_acompanyaments: str
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
            self.employment_situation or self.value_if_empty,
            self.birth_place or self.value_if_empty,
            self.educational_level or self.value_if_empty,
            self.discovered_us or self.value_if_empty,
            self.user_email or self.value_if_empty,
            self.user_phone_number or self.value_if_empty,
            self.user_project or self.value_if_empty,
            self.user_acompanyaments or self.value_if_empty,
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


@dataclass
class InsercioLaboralRow(BaseRow):
    actuacio_reference: str
    user_surname: str
    user_name: str
    user_id_number: str
    insercio_data_alta: str
    insercio_data_baixa: str
    insercio_tipus_contracte: str
    user_gender: str
    user_birthdate: str
    user_town: str
    project_nif: str
    project_name: str
    insercio_cercle: str
    subsidy_period: str
    value_if_empty = "-"

    def get_columns(self) -> list:
        return [
            self.actuacio_reference or self.value_if_empty,
            "",  # Activity name: we need it empty, the excel will fill it
            self.user_surname or self.value_if_empty,
            self.user_name or self.value_if_empty,
            self.user_id_number or self.value_if_empty,
            self.insercio_data_alta or self.value_if_empty,
            self.insercio_data_baixa or self.value_if_empty,
            self.insercio_tipus_contracte or self.value_if_empty,
            self.user_gender or self.value_if_empty,
            self.user_birthdate or self.value_if_empty,
            self.user_town or self.value_if_empty,
            self.project_nif or self.value_if_empty,
            self.project_name or self.value_if_empty,
            self.insercio_cercle or self.value_if_empty,
            self.subsidy_period or self.value_if_empty,
        ]


@dataclass
class CreatedEntityRow(BaseRow):
    actuacio_reference: str
    project_name: str
    project_nif: str
    project_contact_details: str
    project_email: str
    project_phone: str
    actuacio_circle: str
    project_stages_list: str
    value_if_empty = "-"

    def get_columns(self) -> list:
        return [
            self.actuacio_reference or self.value_if_empty,
            "",  # Activity name: we need it empty, the excel will fill it
            self.project_name or self.value_if_empty,
            self.project_nif or self.value_if_empty,
            self.project_contact_details or self.value_if_empty,
            self.project_email or self.value_if_empty,
            self.project_phone or self.value_if_empty,
            "Sí",  # Economia Social i Solidària (no tenim la dada)
            self.actuacio_circle or self.value_if_empty,
            self.project_stages_list or self.value_if_empty,
        ]


@dataclass
class AcompanyamentRow(BaseRow):
    actuacio_reference: str
    project_name: str
    project_status: str
    stage_type: str
    start_date: str
    town: str
    short_description: str
    total_hours: str
    latest_session_date: str
    justification_documents_total: str
    value_if_empty = "-"

    def get_columns(self) -> list:
        return [
            self.actuacio_reference or self.value_if_empty,
            "",  # Activity name: we need it empty, the excel will fill it
            "Entitat",  # No tenim la dada; hardcodejat
            self.project_name or self.value_if_empty,
            self.project_status or self.value_if_empty,
            self.stage_type or self.value_if_empty,  # Crea o Consolida
            self.start_date or self.value_if_empty,
            self.town or self.value_if_empty,
            self.short_description or self.value_if_empty,
            self.total_hours or self.value_if_empty,
            self.latest_session_date or self.value_if_empty,
            self.justification_documents_total or self.value_if_empty,
        ]
