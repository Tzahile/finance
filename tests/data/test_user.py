import hypothesis.strategies as st
from hypothesis import given, infer

from data.user import User


@given(st.builds(User, _id=infer))
def test_get_doc(user: User):
    user_doc = user.get_doc()

    if user.uid:
        assert "_id" in user_doc
    else:
        assert "_id" not in user_doc


@given(st.builds(User, _id=infer))
def test_to_json(user: User):
    user_json = user.to_json()
    loaded_json = User.from_json(user_json)
    assert loaded_json == user
