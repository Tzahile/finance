from datetime import datetime as dt
from typing import Type, List

from bson import ObjectId

from model.normalized_data import NormalizedData
from model.base_crud_dao import BaseCrudDao


class NormalizedDataDao(BaseCrudDao):
    def get_odm(self) -> Type[NormalizedData]:
        return NormalizedData

    def get_user_actions_in_range(
        self, user_id: ObjectId, start_date: dt = None, end_date: dt = None
    ) -> List[NormalizedData]:

        query = {"user_id": user_id}

        if start_date or end_date:
            query["date"] = {}

        if start_date:
            query["date"]["$gte"] = start_date

        if end_date:
            query["date"]["$lt"] = end_date

        return list(map(NormalizedData.to_model, self.get_odm().objects.get_queryset().raw(query)))
