from typing import Dict, List

from pymongo.results import UpdateResult, DeleteResult, InsertManyResult
from pymongo.errors import OperationFailure
from pymongo.database import Database
from pymongo.cursor import Cursor
from pymongo import MongoClient
from bson import ObjectId

from utils.configuration import config


mongo_config = config.get("MONGO", {})
client = MongoClient(mongo_config.get("URI"))


def get_db(db_name: str = None) -> Database:
    if not db_name:
        return client[mongo_config.get("FINANCE_DB")]
    return client[db_name]


def create(collection_name: str, entity: Dict) -> bool:
    status = get_db()[collection_name].insert_one(entity)

    if not status.acknowledged:
        raise OperationFailure("Failed inserting doc")
    return status.acknowledged


def insert_bulk(collection_name: str, bulk: List) -> InsertManyResult:
    return get_db()[collection_name].insert_many(bulk)


def get(collection_name: str, entity_id: ObjectId) -> Dict:
    return get_db()[collection_name].find({"_id": entity_id}).next()


def get_by_query(collection_name: str, query: Dict) -> Cursor:
    return get_db()[collection_name].find(query)


def remove(collection_name: str, entity_id: ObjectId) -> DeleteResult:
    status = get_db()[collection_name].delete_one({"_id": entity_id})

    if not status.acknowledged:
        raise OperationFailure("Failed deleting doc")
    return status


def update(collection_name: str, entity: Dict) -> UpdateResult:
    entity_id = entity["_id"]
    return get_db()[collection_name].update_one({"_id": entity_id}, {"$set": entity})
