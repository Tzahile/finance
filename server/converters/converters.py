from typing import List
from pandas import DataFrame

from class_registry import ClassRegistry

from data.data_class_types import DataclassTypes
from data.normalized_data import NormalizedData

registered_converters = ClassRegistry("provider", unique=True)


def convert_list(bulk: List) -> List[NormalizedData]:
    normalized_data_list = []
    df = DataFrame(obj.to_doc() for obj in bulk)
    for provider_type in DataclassTypes:
        normalized_data_list.extend(
            registered_converters.get(provider_type).convert_dataframe(df[df["_cls"] == provider_type])
        )
    return normalized_data_list
