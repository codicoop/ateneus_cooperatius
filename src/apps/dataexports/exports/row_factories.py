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
