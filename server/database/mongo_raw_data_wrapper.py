from typing import Iterable, Generator, Callable, Dict
from bson import ObjectId
from pymongo.results import UpdateResult, DeleteResult, InsertManyResult

from database import mongo_crud_wrapper
from data.ordernet_api_data import BaseData, data_types

COLLECTION_NAME = mongo_crud_wrapper.mongo_config.get("RAW_DATA_COLLECTION")


def create(raw_data: BaseData) -> BaseData:
    raw_data_doc = raw_data.to_doc()
    mongo_crud_wrapper.create(COLLECTION_NAME, raw_data_doc)
    return raw_data.from_doc(raw_data_doc)


def insert_bulk(bulk: Iterable[BaseData]) -> InsertManyResult:
    doc_bulk = (item.to_doc() for item in bulk)
    return mongo_crud_wrapper.insert_bulk(COLLECTION_NAME, doc_bulk)


def _from_doc_func(cls_name: str) -> Callable[[Dict], BaseData]:
    concrete_class: BaseData = data_types.get_class(cls_name)
    return concrete_class.from_doc


def get(raw_data_id: ObjectId) -> BaseData:
    doc = mongo_crud_wrapper.get(COLLECTION_NAME, raw_data_id)
    from_doc = _from_doc_func(doc["_cls"])
    return from_doc(doc)


def get_bulk_by_user(user_id: ObjectId) -> Generator[BaseData, None, None]:
    query = {"user_id": user_id}
    docs = mongo_crud_wrapper.get_by_query(COLLECTION_NAME, query)
    return (_from_doc_func(doc["_cls"])(doc) for doc in docs)


def remove(raw_data_id: ObjectId) -> DeleteResult:
    return mongo_crud_wrapper.remove(COLLECTION_NAME, raw_data_id)


def update(raw_data: BaseData) -> UpdateResult:
    raw_data_doc = raw_data.to_doc()
    return mongo_crud_wrapper.update(COLLECTION_NAME, raw_data_doc)
