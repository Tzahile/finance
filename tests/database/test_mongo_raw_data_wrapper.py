from typing import List
import unittest
import pytest

from pymongo.errors import DuplicateKeyError
import hypothesis.strategies as st
from hypothesis import given, infer
from bson import ObjectId
import mongomock

from data.psagot_raw_data import PsagotRawData
from database import mongo_raw_data_wrapper
from database import mongo_crud_wrapper


object_id = ObjectId()


class TestMongoUserWrapper(unittest.TestCase):
    @staticmethod
    def setup_example() -> None:
        mongo_crud_wrapper.client = mongomock.MongoClient()

    @given(st.builds(PsagotRawData, _id=infer))
    def test_create_and_get(self, raw_data: PsagotRawData):
        new_raw_data = mongo_raw_data_wrapper.create(raw_data)

        if not raw_data.uid:
            raw_data.uid = new_raw_data.uid
        self.assertEqual(raw_data, new_raw_data)

        retrieved_user = mongo_raw_data_wrapper.get(new_raw_data.uid)
        self.assertEqual(retrieved_user, new_raw_data)

    @given(st.from_type(PsagotRawData))
    def test_create_raise_duplicated_key_error(self, raw_data: PsagotRawData):
        new_raw_data = mongo_raw_data_wrapper.create(raw_data)
        self.assertRaises(DuplicateKeyError, mongo_raw_data_wrapper.create, new_raw_data)

    def test_get_not_existing(self):
        self.assertRaises(StopIteration, mongo_raw_data_wrapper.get, ObjectId())

    @given(st.builds(PsagotRawData, _id=infer))
    def test_create_and_remove(self, raw_data: PsagotRawData):
        created_raw_data = mongo_raw_data_wrapper.create(raw_data)

        status = mongo_raw_data_wrapper.remove(created_raw_data.uid)
        self.assertEqual(status.acknowledged, True)
        self.assertEqual(status.deleted_count, 1)

        with pytest.raises(StopIteration):
            mongo_raw_data_wrapper.get(created_raw_data.uid)

    @given(st.builds(PsagotRawData, _id=infer), st.from_type(PsagotRawData))
    def test_update(self, raw_data: PsagotRawData, updated_raw_data):
        created_raw_data = mongo_raw_data_wrapper.create(raw_data)

        updated_raw_data.uid = created_raw_data.uid

        ret_val = mongo_raw_data_wrapper.update(updated_raw_data)
        self.assertEqual(ret_val.matched_count, 1)

        if updated_raw_data == created_raw_data:
            self.assertEqual(ret_val.modified_count, 0)
        else:
            self.assertEqual(ret_val.modified_count, 1)

        self.assertEqual(ret_val.acknowledged, True)

        retrieved_raw_data = mongo_raw_data_wrapper.get(created_raw_data.uid)

        self.assertEqual(retrieved_raw_data, updated_raw_data)

    @given(st.lists(st.builds(PsagotRawData, user_id=st.sampled_from([ObjectId()]))))
    def test_get_user_raw_data_in_range(self, raw_data_list: List[PsagotRawData]):
        result = mongo_raw_data_wrapper.insert_bulk(raw_data_list)
        self.assertEqual(len(result.inserted_ids), len(raw_data_list))

        bulk_by_user = []
        if raw_data_list:
            user_id = raw_data_list[0].user_id
            bulk_by_user = list(mongo_raw_data_wrapper.get_bulk_by_user(user_id))

        self.assertEqual(len(bulk_by_user), len(raw_data_list))
