from typing import Iterable, Generator
from datetime import datetime as dt

from pymongo.results import UpdateResult, DeleteResult, InsertManyResult
from bson import ObjectId

from database import mongo_crud_wrapper
from data.normalized_data import NormalizedData


COLLECTION_NAME = mongo_crud_wrapper.mongo_config.get("NORMELIZED_DATA_COLLECTION")


def create(raw_data: NormalizedData) -> NormalizedData:
    raw_data_doc = raw_data.get_doc()
    mongo_crud_wrapper.create(COLLECTION_NAME, raw_data_doc)
    return NormalizedData(**raw_data_doc)


def insert_bulk(bulk: Iterable[NormalizedData]) -> InsertManyResult:
    doc_bulk = (item.get_doc() for item in bulk)
    return mongo_crud_wrapper.insert_bulk(COLLECTION_NAME, doc_bulk)


def get(raw_data_id: ObjectId) -> NormalizedData:
    raw_data_id_doc = mongo_crud_wrapper.get(COLLECTION_NAME, raw_data_id)
    return NormalizedData(**raw_data_id_doc)


def get_bulk_by_user(user_id: ObjectId) -> Generator[NormalizedData, None, None]:
    query = {"user_id": user_id}
    raw_data_results = mongo_crud_wrapper.get_by_query(COLLECTION_NAME, query)
    return (NormalizedData(**result) for result in raw_data_results)


def remove(raw_data_id: ObjectId) -> DeleteResult:
    return mongo_crud_wrapper.remove(COLLECTION_NAME, raw_data_id)


def update(raw_data: NormalizedData) -> UpdateResult:
    raw_data_doc = raw_data.get_doc()
    return mongo_crud_wrapper.update(COLLECTION_NAME, raw_data_doc)


def get_user_normalized_data_in_range(
    user_id: ObjectId, start_date: dt = None, end_date: dt = None
) -> Generator[NormalizedData, None, None]:

    query = {"user_id": user_id}

    if start_date or end_date:
        query["date"] = {}

    if start_date:
        query["date"]["$gte"] = start_date

    if end_date:
        query["date"]["$lt"] = end_date

    raw_data_results = mongo_crud_wrapper.get_by_query(COLLECTION_NAME, query)
    return (NormalizedData(**result) for result in raw_data_results)
