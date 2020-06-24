from abc import abstractmethod
from typing import Dict

from bson.errors import InvalidId
from pymodm import MongoModel

from database.mongo_connector import BaseMongo
from utils.utils import to_object_id


class BaseCrudDao(BaseMongo):
    @abstractmethod
    def get_odm(self) -> MongoModel:
        raise NotImplementedError("Not Implemented")

    def create(self, entity: Dict) -> MongoModel:
        entity_copy = entity.copy()
        BaseCrudDao.prepare_id(entity_copy)
        return self.get_odm().from_document(entity_copy).save().to_model()

    def get(self, entity_id: str) -> MongoModel:
        return self.get_odm().objects.get_queryset().get({"_id": to_object_id(entity_id)}).to_model()

    def delete(self, entity_id: str) -> None:
        self.get_odm().objects.get_queryset().get({"_id": to_object_id(entity_id)}).delete()

    def update(self, entity: Dict) -> int:
        entity_copy = entity.copy()
        entity_id = entity_copy.pop("id", None)
        return (
            self.get_odm()
            .objects.get_queryset()
            .raw({"_id": to_object_id(entity_id)})
            .update({"$set": entity_copy}, upsert=True)
        )

    @staticmethod
    def prepare_id(entity: Dict) -> None:
        try:
            entity["_id"] = to_object_id(entity.pop("id", None))

        except InvalidId:
            entity.pop("id", None)
            entity.pop("_id", None)
