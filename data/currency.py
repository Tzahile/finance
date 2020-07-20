from enum import Enum, auto, unique


@unique
class Currency(Enum):
    ILS = auto()
    USD = auto()
