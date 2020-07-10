from typing import List
from bson import ObjectId
from pymongo.results import UpdateResult, DeleteResult, InsertManyResult

from database import mongo_crud_wrapper
from data.psagot_raw_data import PsagotRawData


COLLECTION_NAME = mongo_crud_wrapper.mongo_config.get("RAW_DATA_COLLECTION")


def create(raw_data: PsagotRawData) -> PsagotRawData:
    raw_data_doc = raw_data.get_doc()
    mongo_crud_wrapper.create(COLLECTION_NAME, raw_data_doc)
    return PsagotRawData(**raw_data_doc)


def insert_bulk(bulk: List[PsagotRawData]) -> InsertManyResult:
    doc_bulk = [item.get_doc() for item in bulk]
    if doc_bulk:
        return mongo_crud_wrapper.insert_bulk(COLLECTION_NAME, doc_bulk)
    return InsertManyResult([], True)


def get(raw_data_id: ObjectId) -> PsagotRawData:
    raw_data_id_doc = mongo_crud_wrapper.get(COLLECTION_NAME, raw_data_id)
    return PsagotRawData(**raw_data_id_doc)


def get_bulk_by_user(user_id: ObjectId) -> List[PsagotRawData]:
    query = {"user_id": user_id}
    raw_data_results = mongo_crud_wrapper.get_by_query(COLLECTION_NAME, query)
    return [PsagotRawData(**result) for result in raw_data_results]


def remove(raw_data_id: ObjectId) -> DeleteResult:
    return mongo_crud_wrapper.remove(COLLECTION_NAME, raw_data_id)


def update(raw_data: PsagotRawData) -> UpdateResult:
    raw_data_doc = raw_data.get_doc()
    return mongo_crud_wrapper.update(COLLECTION_NAME, raw_data_doc)
