# pylint: disable=no-value-for-parameter
from typing import List
from datetime import datetime
from datetime import timedelta
import unittest

from pymongo.errors import DuplicateKeyError
import hypothesis.strategies as st
from hypothesis import given
from bson import ObjectId
import mongomock
import pytest

from data.normalized_data import NormalizedData
from database import mongo_normalized_data_wrapper
from database import mongo_crud_wrapper


@st.composite
def rounded_datetime(draw) -> datetime:
    generated_datetime = draw(st.datetimes())
    return generated_datetime - timedelta(microseconds=generated_datetime.microsecond)


normalized_data_strategy = st.builds(NormalizedData, date=rounded_datetime())


class TestMongoUserWrapper(unittest.TestCase):
    @staticmethod
    def setup_example() -> None:
        mongo_crud_wrapper.client = mongomock.MongoClient()

    @given(normalized_data_strategy)
    def test_create_and_get(self, normalized_data: NormalizedData):
        new_normalized_data = mongo_normalized_data_wrapper.create(normalized_data)

        normalized_data.uid = new_normalized_data.uid
        self.assertEqual(normalized_data, new_normalized_data)

        retrieved_user = mongo_normalized_data_wrapper.get(new_normalized_data.uid)
        self.assertEqual(retrieved_user, new_normalized_data)

    @given(st.from_type(NormalizedData))
    def test_create_raise_duplicated_key_error(self, normalized_data: NormalizedData):
        new_normalized_data = mongo_normalized_data_wrapper.create(normalized_data)
        self.assertRaises(DuplicateKeyError, mongo_normalized_data_wrapper.create, new_normalized_data)

    @given(st.from_type(ObjectId))
    def test_get_not_existing(self, object_id):
        self.assertRaises(StopIteration, mongo_normalized_data_wrapper.get, object_id)

    @given(normalized_data_strategy)
    def test_create_and_remove(self, normalized_data: NormalizedData):
        created_normalized_data = mongo_normalized_data_wrapper.create(normalized_data)

        status = mongo_normalized_data_wrapper.remove(created_normalized_data.uid)
        self.assertEqual(status.acknowledged, True)
        self.assertEqual(status.deleted_count, 1)

        with pytest.raises(StopIteration):
            mongo_normalized_data_wrapper.get(created_normalized_data.uid)

    @given(normalized_data_strategy, normalized_data_strategy)
    def test_update(self, normalized_data: NormalizedData, updated_normalized_data):
        created_normalized_data = mongo_normalized_data_wrapper.create(normalized_data)

        updated_normalized_data.uid = created_normalized_data.uid

        ret_val = mongo_normalized_data_wrapper.update(updated_normalized_data)
        self.assertEqual(ret_val.matched_count, 1)

        if updated_normalized_data == created_normalized_data:
            self.assertEqual(ret_val.modified_count, 0)
        else:
            self.assertEqual(ret_val.modified_count, 1)

        self.assertEqual(ret_val.acknowledged, True)

        retrieved_normalized_data = mongo_normalized_data_wrapper.get(created_normalized_data.uid)

        self.assertEqual(retrieved_normalized_data, updated_normalized_data)

    @given(st.lists(st.builds(NormalizedData, date=rounded_datetime(), user_id=st.sampled_from([ObjectId()]))))
    def test_get_bulk_by_user(self, normalized_data_list: List[NormalizedData]):
        result = mongo_normalized_data_wrapper.insert_bulk(normalized_data_list)
        self.assertEqual(len(result.inserted_ids), len(normalized_data_list))

        bulk_by_user = []
        if normalized_data_list:
            user_id = normalized_data_list[0].user_id
            bulk_by_user = list(mongo_normalized_data_wrapper.get_bulk_by_user(user_id))

        self.assertEqual(len(bulk_by_user), len(normalized_data_list))

    @given(st.lists(st.builds(NormalizedData, date=rounded_datetime(), user_id=st.sampled_from([ObjectId()]))))
    def test_get_user_normalized_data_in_range(self, normalized_data_list: List[NormalizedData]):
        result = mongo_normalized_data_wrapper.insert_bulk(normalized_data_list)
        self.assertEqual(len(result.inserted_ids), len(normalized_data_list))

        sorted_normalized_data_list = sorted(normalized_data_list, key=lambda item: item.date)

        retrieved_list_all = []

        retrieved_trim_last_date = []
        trim_last_date_list = []

        retrieved_trim_first_date = []
        trim_first_date_list = []

        if sorted_normalized_data_list:
            user_id = sorted_normalized_data_list[0].user_id
            first_date = sorted_normalized_data_list[0].date
            last_date = sorted_normalized_data_list[-1].date

            retrieved_list_all = mongo_normalized_data_wrapper.get_user_normalized_data_in_range(
                user_id, first_date, last_date + timedelta(days=1)
            )

            retrieved_trim_last_date = mongo_normalized_data_wrapper.get_user_normalized_data_in_range(
                user_id, first_date, last_date
            )

            trim_last_date_list = list(filter(lambda x: x.date < last_date, sorted_normalized_data_list))

            retrieved_trim_first_date = mongo_normalized_data_wrapper.get_user_normalized_data_in_range(
                user_id, first_date + timedelta(days=1), last_date
            )

            trim_first_date_list = list(
                filter(lambda x: first_date + timedelta(days=1) <= x.date < last_date, sorted_normalized_data_list)
            )

        # all
        self.assertEqual(len(list(retrieved_list_all)), len(sorted_normalized_data_list))

        # to last date
        self.assertEqual(len(list(retrieved_trim_last_date)), len(trim_last_date_list))

        # from first date + 1
        self.assertEqual(len(list(retrieved_trim_first_date)), len(trim_first_date_list))
