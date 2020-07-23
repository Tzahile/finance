import hypothesis.strategies as st
from hypothesis import given
from bson import ObjectId

from data.ordernet_api_data import OrdernetApiData


real_float = st.floats(allow_infinity=False, allow_nan=False)


@given(st.from_type(OrdernetApiData), st.one_of(st.from_type(ObjectId), st.none()))
def test_get_doc(psagot_raw_data: OrdernetApiData, object_id):
    psagot_raw_data.uid = object_id
    psagot_raw_data_doc = psagot_raw_data.to_doc()
    data_obj = OrdernetApiData.from_doc(psagot_raw_data_doc)
    assert data_obj == psagot_raw_data


@given(
    st.builds(OrdernetApiData, i=real_float, k=real_float, l=real_float, m=real_float, n=real_float, o=real_float),
    st.one_of(st.from_type(ObjectId), st.none()),
)
def test_to_json(psagot_raw_data: OrdernetApiData, object_id):
    psagot_raw_data.uid = object_id
    psagot_raw_data_json = psagot_raw_data.to_json()
    loaded_json = OrdernetApiData.from_json(psagot_raw_data_json)
    assert loaded_json == psagot_raw_data
