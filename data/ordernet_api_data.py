from __future__ import annotations

from dataclasses import dataclass, field

from bson import ObjectId

from data.base_data import data_types, BaseData
from data.data_class_types import DataclassTypes


@data_types.register
@dataclass
class OrdernetApiData(BaseData):
    _t: str  # type
    a: str  # account_number
    b: str  # date
    c: str  # paper_or_transaction_num
    d: str  # refernce_number
    e: str  # unkown
    f: str  # paper_or_transactionv
    i: float  # quantity
    j: str  # action
    k: float  # cash_balance
    l: float  # commission
    m: float  # cost
    n: float  # zhut_neto
    o: float  # hova_neto

    user_id: ObjectId
    _cls: DataclassTypes = field(init=False, default=DataclassTypes.ORDERNET_API)
