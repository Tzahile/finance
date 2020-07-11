# pylint: disable=no-value-for-parameter
from datetime import timedelta
from datetime import datetime

import hypothesis.strategies as st
from hypothesis import given, infer

from data.normalized_data import NormalizedData


real_float = st.floats(allow_infinity=False, allow_nan=False)


@st.composite
def rounded_datetime(draw) -> datetime:
    generated_datetime = draw(st.datetimes())
    return generated_datetime - timedelta(microseconds=generated_datetime.microsecond)


@given(st.builds(NormalizedData, _id=infer, raw_data_id=infer))
def test_get_doc(normalized_data: NormalizedData):
    normalized_data_doc = normalized_data.get_doc()

    if normalized_data.uid:
        assert "_id" in normalized_data_doc
    else:
        assert "_id" not in normalized_data_doc


@given(
    st.builds(
        NormalizedData,
        _id=infer,
        raw_data_id=infer,
        cash_balance=real_float,
        commission=real_float,
        quantity=real_float,
        cost=real_float,
        date=rounded_datetime(),
    )
)
def test_to_json(normalized_data: NormalizedData):
    normalized_data_json = normalized_data.to_json()
    loaded_json = NormalizedData.from_json(normalized_data_json)
    assert loaded_json == normalized_data
