from enum import Enum
from typing import List


class Column(Enum):
    DATE = ('b', 'date')
    PAPER_OR_TRANSACTION_NUM = ('c', 'paper_or_transaction_num')
    PAPER_OR_TRANSACTION = ('f', 'paper_or_transaction')
    QUANTITY = ('i', 'quantity')
    ACTION = ('j', 'action')
    CASH_BALANCE = ('k', 'cash_balance')
    COMMISSION = ('l', 'commission')
    COST = ('m', 'cost')
    ZHUT = ('n', 'zhut_neto')
    HOVA = ('o', 'hova_neto')

    @property
    def value(self) -> str:
        return self._value_[1]

    @property
    def json_field(self) -> str:
        return self._value_[0]

    @staticmethod
    def translate(field: str) -> str:
        for tup in Column.__members__.values():
            if tup.json_field == field:
                return tup.value
        raise ValueError(f'field \'{field}\' is illegal.')

    @staticmethod
    def bad_fields() -> List[str]:
        return ['_t', 'a', 'e', 'd']
