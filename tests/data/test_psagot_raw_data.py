import hypothesis.strategies as st
from hypothesis import given, infer

from data.psagot_raw_data import PsagotRawData


real_float = st.floats(allow_infinity=False, allow_nan=False)


@given(st.builds(PsagotRawData, _id=infer))
def test_get_doc(psagot_raw_data: PsagotRawData):
    psagot_raw_data_doc = psagot_raw_data.get_doc()

    if psagot_raw_data.uid:
        assert "_id" in psagot_raw_data_doc
    else:
        assert "_id" not in psagot_raw_data_doc


@given(
    st.builds(
        PsagotRawData, _id=infer, i=real_float, k=real_float, l=real_float, m=real_float, n=real_float, o=real_float
    )
)
def test_to_json(psagot_raw_data: PsagotRawData):
    psagot_raw_data_json = psagot_raw_data.to_json()
    loaded_json = PsagotRawData.from_json(psagot_raw_data_json)
    assert loaded_json == psagot_raw_data
