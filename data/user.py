from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, Optional
import json

from bson import ObjectId, json_util


@dataclass
class User:
    first_name: str
    last_name: str
    _id: Optional[ObjectId] = None

    @property
    def uid(self) -> ObjectId:
        return self._id

    @uid.setter
    def uid(self, uid: ObjectId) -> None:
        self._id = uid

    def get_doc(self) -> Dict:
        user_doc = self.__dict__.copy()
        if self._id is None:
            user_doc.pop("_id")
        return user_doc

    def to_json(self) -> str:
        return json.dumps(asdict(self), default=json_util.default)

    @staticmethod
    def from_json(json_user: str) -> User:
        return User(**json.loads(json_user, object_hook=json_util.object_hook))
