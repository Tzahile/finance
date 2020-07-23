from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, cast
from datetime import datetime

from bson import ObjectId

from data.base_data import BaseData, data_types
from data.data_class_types import DataclassTypes


@data_types.register
@dataclass
class NormalizedData(BaseData):
    user_id: ObjectId
    paper_id: str
    transaction_id: str
    paper: str
    transaction: str
    quantity: float
    action: str
    cash_balance: float
    commission: float
    cost: float
    date: datetime

    raw_data_id: Optional[ObjectId] = None
    _cls: DataclassTypes = field(init=False, default=DataclassTypes.NORMALIZED_DATA)

    @staticmethod
    def from_json(json_data: str) -> NormalizedData:
        obj: NormalizedData = cast(NormalizedData, BaseData.from_json(json_data))
        obj.date = obj.date.replace(tzinfo=None, microsecond=0)
        return obj
