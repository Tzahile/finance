from __future__ import annotations
from dataclasses import dataclass, field

from bson import ObjectId

from data.base_data import BaseData, data_types
from data.data_class_types import DataclassTypes


@data_types.register
@dataclass
class OrdernetExcelData(BaseData):
    date: str
    paper_or_transaction: str
    paper_id_or_transaction_id: int
    action: str
    quantity: float
    cost: float
    net_credit: float
    net_owe: float
    commission: float
    cash_balance: float
    reference: str
    user_id: ObjectId

    _cls: DataclassTypes = field(init=False, default=DataclassTypes.ORDERNET_EXCEL)
