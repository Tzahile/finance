from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, Optional
from datetime import datetime
import json

from bson import ObjectId, json_util


@dataclass
class NormalizedData:
    user_id: ObjectId
    paper_num: int
    transaction_num: int
    paper: str
    transaction: str
    quantity: int
    action: str
    cash_balance: float
    commission: float
    cost: float
    _date: datetime
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
        date_str = normalized_data.date.strftime('%Y-%m-%dT%H:%M:%S')
        normalized_data.date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
        return normalized_data
