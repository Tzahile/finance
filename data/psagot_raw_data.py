from __future__ import annotations
from dataclasses import dataclass, asdict, field
from typing import Dict, Optional
import json

from bson import ObjectId, json_util


@dataclass
class PsagotRawData:
    _t: str  # type
    a: str  # account_number
    b: str  # date
    c: int  # paper_or_transaction_num
    d: int  # refernce_number
    e: int  # unkown
    f: str  # paper_or_transactionv
    i: float  # quantity
    j: str  # action
    k: float  # cash_balance
    l: float  # commission
    m: float  # cost
    n: float  # zhut_neto
    o: float  # hova_neto
    user_id: ObjectId
    _cls: str = field(init=False)
    _id: Optional[ObjectId] = None

    def __post_init__(self):
        self._cls = self.__class__.__name__

    @property
    def uid(self) -> ObjectId:
        return self._id

    @uid.setter
    def uid(self, uid: ObjectId) -> None:
        self._id = uid

    def get_doc(self) -> Dict:
        raw_data_doc = asdict(self).copy()
        if self._id is None:
            raw_data_doc.pop("_id")
        return raw_data_doc

    def to_json(self) -> str:
        return json.dumps(asdict(self), default=json_util.default)

    @staticmethod
    def from_json(json_data: str) -> PsagotRawData:
        loaded_json = json.loads(json_data, object_hook=json_util.object_hook)
        loaded_json.pop("_cls", None)
        return PsagotRawData(**loaded_json)
