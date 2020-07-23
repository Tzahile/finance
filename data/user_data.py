from __future__ import annotations
from dataclasses import dataclass, field

from data.base_data import BaseData, data_types
from data.data_class_types import DataclassTypes


@data_types.register
@dataclass
class UserData(BaseData):
    first_name: str
    last_name: str

    _cls: DataclassTypes = field(init=False, default=DataclassTypes.USER_DATA)
