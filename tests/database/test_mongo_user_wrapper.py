import unittest
import pytest

from pymongo.errors import DuplicateKeyError
import hypothesis.strategies as st
from hypothesis import given
from bson import ObjectId
import mongomock

from data.user_data import UserData
from database import mongo_user_wrapper
from database import mongo_crud_wrapper


class TestMongoUserWrapper(unittest.TestCase):
    def setUp(self) -> None:
        mongo_crud_wrapper.client = mongomock.MongoClient()

    @given(st.builds(UserData))
    def test_create_and_get(self, user: UserData):
        new_user = mongo_user_wrapper.create(user)

        user.uid = new_user.uid
        self.assertEqual(user, new_user)

        retrieved_user = mongo_user_wrapper.get(new_user.uid)
        self.assertEqual(retrieved_user, new_user)

    @given(st.from_type(UserData))
    def test_create_raise_duplicated_key_error(self, user: UserData):
        new_user = mongo_user_wrapper.create(user)
        self.assertRaises(DuplicateKeyError, mongo_user_wrapper.create, new_user)

    @given(st.from_type(ObjectId))
    def test_get_not_existing(self, object_id):
        self.assertRaises(StopIteration, mongo_user_wrapper.get, object_id)

    @given(st.builds(UserData))
    def test_create_and_remove(self, user: UserData):
        created_user = mongo_user_wrapper.create(user)

        status = mongo_user_wrapper.remove(created_user.uid)
        self.assertEqual(status.acknowledged, True)
        self.assertEqual(status.deleted_count, 1)

        with pytest.raises(StopIteration):
            mongo_user_wrapper.get(created_user.uid)

    @given(st.builds(UserData), st.from_type(UserData))
    def test_update(self, user: UserData, updated_user):
        created_user = mongo_user_wrapper.create(user)

        updated_user.uid = created_user.uid

        ret_val = mongo_user_wrapper.update(updated_user)
        self.assertEqual(ret_val.matched_count, 1)

        if updated_user == created_user:
            self.assertEqual(ret_val.modified_count, 0)
        else:
            self.assertEqual(ret_val.modified_count, 1)

        self.assertEqual(ret_val.acknowledged, True)

        retrieved_user = mongo_user_wrapper.get(created_user.uid)

        self.assertEqual(retrieved_user, updated_user)
