from enum import IntEnum, unique, auto


@unique
class Provider(IntEnum):
    ORDERNET = auto()
