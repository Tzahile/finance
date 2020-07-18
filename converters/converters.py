from typing import List
from pandas import DataFrame

from class_registry import ClassRegistry

from data.common import Provider
from data.normalized_data import NormalizedData

registered_converters = ClassRegistry("provider", unique=True)


def convert_list(bulk: List) -> List[NormalizedData]:
    normalized_data_list = []
    df = DataFrame(obj.get_doc() for obj in bulk)
    for provider_type in Provider:
        normalized_data_list.extend(
            registered_converters.get(provider_type).convert_dataframe(df[df["_provider"] == provider_type])
        )
    return normalized_data_list
