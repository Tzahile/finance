# pylint: disable=no-value-for-parameter
from datetime import timedelta
from datetime import datetime

import hypothesis.strategies as st
from hypothesis import given, infer
from bson import ObjectId

from data.normalized_data import NormalizedData


real_float = st.floats(allow_infinity=False, allow_nan=False)


@st.composite
def rounded_datetime(draw) -> datetime:
    generated_datetime = draw(st.datetimes())
    return generated_datetime - timedelta(microseconds=generated_datetime.microsecond)


@given(st.builds(NormalizedData, raw_data_id=infer), st.one_of(st.from_type(ObjectId), st.none()))
def test_get_doc(normalized_data: NormalizedData, object_id):
    normalized_data.uid = object_id
    normalized_data_doc = normalized_data.to_doc()
    data_obj = NormalizedData.from_doc(normalized_data_doc)
    assert data_obj == normalized_data


@given(
    st.builds(
        NormalizedData,
        raw_data_id=infer,
        cash_balance=real_float,
        commission=real_float,
        quantity=real_float,
        cost=real_float,
        date=rounded_datetime(),
    ),
    st.one_of(st.from_type(ObjectId), st.none()),
)
def test_to_json(normalized_data: NormalizedData, object_id):
    normalized_data.uid = object_id
    normalized_data_json = normalized_data.to_json()
    loaded_json = NormalizedData.from_json(normalized_data_json)
    assert loaded_json == normalized_data
