from __future__ import annotations

from pymodm import MongoModel, fields
from utils.configuration import Configurations


class User(MongoModel):
    id = fields.CharField()
    first_name = fields.CharField()
    last_name = fields.CharField()

    def to_model(self) -> User:
        odm_dict = self.to_son()
        odm_dict["id"] = str(odm_dict.pop("_id"))
        del odm_dict["_cls"]
        return User(**odm_dict)

    class Meta:
        connection_alias = Configurations().mongo.get("ALIAS", "default")
