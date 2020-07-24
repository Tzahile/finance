from typing import List

from pandas import DataFrame

from converters.converters import registered_converters
from converters.base_converter import BaseConverter
from data.normalized_data import NormalizedData
from data.data_class_types import DataclassTypes


@registered_converters.register
class OrdernetConverter(BaseConverter):
    provider = DataclassTypes.ORDERNET_API

    mapping = {
        "date": {"name": "b", "pipeline": []},
        "paper_id": {"name": "c", "pipeline": []},
        "transaction_id": {"name": "f", "pipeline": []},
        "quantity": {"name": "i", "pipeline": []},
        "action": {"name": "j", "pipeline": []},
        "cash_balance": {"name": "k", "pipeline": []},
        "commission": {"name": "l", "pipeline": []},
        "cost": {"name": "m", "pipeline": []},
        "paper": {"name": "n", "pipeline": []},
        "transaction": {"name": "o", "pipeline": []},
        "user_id": {"name": "user_id", "pipeline": []},
        "raw_data_id": {"name": "_id", "pipeline": []},
    }

    def convert_dataframe(self, df: DataFrame) -> List[NormalizedData]:
        name_mapping = {v.get("name"): k for k, v in self.mapping.items()}

        self.fill_missing_columns(df, name_mapping)
        df_ordernet = df[name_mapping.keys()]
        df_ordernet.rename(columns=name_mapping, inplace=True)
        self.run_pipeline(df_ordernet)

        normalized_list = df_ordernet.to_dict(orient="records")

        return [NormalizedData(**item) for item in normalized_list]
