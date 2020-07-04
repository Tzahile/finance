from bson import ObjectId
from pymongo.results import UpdateResult, DeleteResult

from database import mongo_crud_wrapper
from data.user import User


COLLECTION_NAME = mongo_crud_wrapper.mongo_config.get("USER_COLLECTION")


def create(user: User) -> User:
    user_doc = user.get_doc()
    mongo_crud_wrapper.create(COLLECTION_NAME, user_doc)
    return User(**user_doc)


def get(user_id: ObjectId) -> User:
    user_doc = mongo_crud_wrapper.get(COLLECTION_NAME, user_id)
    return User(**user_doc)


def remove(user_id: ObjectId) -> DeleteResult:
    return mongo_crud_wrapper.remove(COLLECTION_NAME, user_id)


def update(user: User) -> UpdateResult:
    user_doc = user.get_doc()
    return mongo_crud_wrapper.update(COLLECTION_NAME, user_doc)
