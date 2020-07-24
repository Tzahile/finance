import hypothesis.strategies as st
from hypothesis import given
from bson import ObjectId

from data.user_data import UserData


@given(st.from_type(UserData), st.one_of(st.from_type(ObjectId), st.none()))
def test_get_doc(user: UserData, object_id):
    user.uid = object_id
    user_doc = user.to_doc()
    data_obj = UserData.from_doc(user_doc)
    assert data_obj == user


@given(st.from_type(UserData), st.one_of(st.from_type(ObjectId), st.none()))
def test_to_json(user: UserData, object_id):
    user.uid = object_id
    user_json = user.to_json()
    loaded_json = UserData.from_json(user_json)
    assert loaded_json == user
