from abc import ABC, abstractmethod
from typing import List, Dict

from pandas import DataFrame

from data.normalized_data import NormalizedData
from data.data_class_types import DataclassTypes


class BaseConverter(ABC):
    @property
    @abstractmethod
    def mapping(self) -> Dict:
        pass

    @property
    @abstractmethod
    def provider(self) -> DataclassTypes:
        pass

    @abstractmethod
    def convert_dataframe(self, df: DataFrame) -> List[NormalizedData]:
        pass

    @staticmethod
    def fill_missing_columns(df: DataFrame, mapping: Dict) -> None:
        for col in mapping:
            if col not in df.columns:
                df[col] = None

    def run_pipeline(self, df: DataFrame) -> None:
        for k, v in self.mapping.items():
            for func in v.get("pipeline", []):
                df[k] = df[k].apply(func)
