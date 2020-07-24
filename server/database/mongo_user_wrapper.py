from bson import ObjectId
from pymongo.results import UpdateResult, DeleteResult

from database import mongo_crud_wrapper
from data.user_data import UserData
from data.base_data import BaseData


COLLECTION_NAME = mongo_crud_wrapper.mongo_config.get("USER_COLLECTION")


def create(user: UserData) -> BaseData:
    user_doc = user.to_doc()
    mongo_crud_wrapper.create(COLLECTION_NAME, user_doc)
    return UserData.from_doc(user_doc)


def get(user_id: ObjectId) -> BaseData:
    user_doc = mongo_crud_wrapper.get(COLLECTION_NAME, user_id)
    return UserData.from_doc(user_doc)


def remove(user_id: ObjectId) -> DeleteResult:
    return mongo_crud_wrapper.remove(COLLECTION_NAME, user_id)


def update(user: UserData) -> UpdateResult:
    user_doc = user.to_doc()
    return mongo_crud_wrapper.update(COLLECTION_NAME, user_doc)
