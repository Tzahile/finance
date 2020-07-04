import unittest
import pytest

from pymongo.errors import DuplicateKeyError
import hypothesis.strategies as st
from hypothesis import given, infer
from bson import ObjectId
import mongomock

from data.user import User
from database import mongo_user_wrapper
from database import mongo_crud_wrapper


class TestMongoUserWrapper(unittest.TestCase):
    def setUp(self) -> None:
        mongo_crud_wrapper.client = mongomock.MongoClient()

    @given(st.builds(User, _id=infer))
    def test_create_and_get(self, user: User):
        new_user = mongo_user_wrapper.create(user)
        self.assertEqual(new_user.first_name, user.first_name)
        self.assertEqual(new_user.last_name, user.last_name)

        if not user.uid:
            user.uid = new_user.uid
        self.assertEqual(user, new_user)

        retrieved_user = mongo_user_wrapper.get(new_user.uid)
        self.assertEqual(retrieved_user, new_user)

    @given(st.from_type(User))
    def test_create_raise_duplicated_key_error(self, user: User):
        new_user = mongo_user_wrapper.create(user)
        self.assertRaises(DuplicateKeyError, mongo_user_wrapper.create, new_user)

    def test_get_not_existing(self):
        self.assertRaises(StopIteration, mongo_user_wrapper.get, ObjectId())

    @given(st.builds(User, _id=infer))
    def test_create_and_remove(self, user: User):
        created_user = mongo_user_wrapper.create(user)

        status = mongo_user_wrapper.remove(created_user.uid)
        self.assertEqual(status.acknowledged, True)
        self.assertEqual(status.deleted_count, 1)

        with pytest.raises(StopIteration):
            mongo_user_wrapper.get(created_user.uid)

    @given(st.builds(User, _id=infer), st.from_type(User))
    def test_update(self, user: User, updated_user):
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
