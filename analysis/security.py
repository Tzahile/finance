from dataclasses import dataclass
from enum import Enum, unique, auto

from pandas import DataFrame
from typing import List, Set
from data import Column


@unique
class Currency(Enum):
    ILS = auto()
    USD = auto()


@dataclass
class Security:
    """
    A trade-able financial asset
    """
    name: str
    identifier: int
    quantity: int
    is_active: bool
    currency: Currency


Securities = List[Security]


def _get_security(df: DataFrame, identifier: int) -> Security:
    # filter data-frame by security-id
    df = df[df[Column.PAPER_OR_TRANSACTION_NUM.value] == identifier]

    # take last value [-1] because security names may change with time
    name: str = df[Column.PAPER_OR_TRANSACTION.value].values[-1]

    quantity: int = 0
    per_action: DataFrame = (df[[Column.ACTION.value, Column.QUANTITY.value]]
                             .groupby(Column.ACTION.value)
                             .sum()
                             .reset_index())
    for index, row in per_action.iterrows():
        if row[Column.ACTION.value] in ['ק/חו"ל', "קניה"]:
            quantity += row[Column.QUANTITY.value]
        else:
            quantity -= row[Column.QUANTITY.value]

    currency = Currency.ILS
    if 0 in df[Column.COMMISSION.value].unique():
        currency = Currency.USD

    return Security(name=name,
                    identifier=identifier,
                    quantity=quantity,
                    is_active=quantity > 0,
                    currency=currency)


def get_securities(df: DataFrame) -> Securities:
    exclude = {
        900,  # for internal actions
        99218,  # dollar commitment
        99028,  # USD
    }
    security_ids: Set[int] = set(df[Column.PAPER_OR_TRANSACTION_NUM.value].unique())
    return [_get_security(df, identifier) for identifier in security_ids - exclude]


def main():
    import data
    from pprint import pprint
    df = data.parse('data.json')
    pprint(get_securities(df))


if __name__ == '__main__':
    main()
