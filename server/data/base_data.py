from __future__ import annotations

import json
from abc import ABC
from dataclasses import dataclass, asdict, field
from typing import Dict, Optional

from bson import ObjectId, json_util
from class_registry import ClassRegistry

from data.data_class_types import DataclassTypes


data_types = ClassRegistry("_cls", unique=True)


@dataclass
class _BaseData(ABC):
    _id: Optional[ObjectId] = field(init=False, default=None)
    _cls: DataclassTypes = field(init=False)

    @property
    def uid(self) -> ObjectId:
        return self._id

    @uid.setter
    def uid(self, uid: ObjectId) -> None:
        self._id = uid

    def to_doc(self) -> Dict:
        raw_data_doc = asdict(self).copy()
        if self._id is None:
            raw_data_doc.pop("_id")
        return raw_data_doc

    def to_json(self) -> str:
        return json.dumps(asdict(self), default=json_util.default)

    @staticmethod
    def from_doc(doc: Dict) -> BaseData:
        class_type = doc.get("_cls")
        doc_copy = {k: v for k, v in doc.items() if k not in _BaseData.__annotations__.keys()}
        obj: BaseData = data_types.get(class_type, **doc_copy)
        obj.uid = doc.get("_id")
        return obj

    @staticmethod
    def from_json(json_data: str) -> BaseData:
        loaded_json = json.loads(json_data, object_hook=json_util.object_hook)
        uid = loaded_json.pop("_id", None)
        class_type = loaded_json.pop("_cls")
        obj: BaseData = data_types.get(class_type, **loaded_json)
        obj.uid = uid
        return obj


class BaseData(_BaseData, ABC):
    """
    The base class for all raw-data types
    An extension of _BaseData for exposing abstract methods
    """

    ...
