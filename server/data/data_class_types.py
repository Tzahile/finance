from enum import IntEnum, unique, auto


@unique
class DataclassTypes(IntEnum):
    ORDERNET_API = auto()
    ORDERNET_EXCEL = auto()
    NORMALIZED_DATA = auto()
    USER_DATA = auto()
