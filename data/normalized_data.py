from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, Optional
from datetime import timedelta
from datetime import datetime
import json

from bson import ObjectId, json_util


@dataclass
class NormalizedData:
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
    _id: Optional[ObjectId] = None

    @property
    def uid(self) -> ObjectId:
        return self._id

    @uid.setter
    def uid(self, uid: ObjectId) -> None:
        self._id = uid

    def get_doc(self) -> Dict:
        normalized_data_doc = asdict(self).copy()
        if self._id is None:
            normalized_data_doc.pop("_id")
        return normalized_data_doc

    def to_json(self) -> str:
        return json.dumps(asdict(self), default=json_util.default)

    @staticmethod
    def from_json(json_normalized_data: str) -> NormalizedData:
        normalized_data = NormalizedData(**json.loads(json_normalized_data, object_hook=json_util.object_hook))
        normalized_data.date = normalized_data.date - timedelta(microseconds=normalized_data.date.microsecond)
        normalized_data.date = normalized_data.date.replace(tzinfo=None)
        return normalized_data
