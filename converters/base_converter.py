from abc import ABC, abstractmethod
from typing import List

from pandas import DataFrame

from data.normalized_data import NormalizedData
from data.common import Provider


class BaseConverter(ABC):
    @property
    @abstractmethod
    def provider(self) -> Provider:
        pass

    @abstractmethod
    def convert_dataframe(self, df: DataFrame) -> List[NormalizedData]:
        pass
