import json
from pandas import DataFrame
from pandas import json_normalize

from data.column import Column


def parse(json_file_path: str) -> DataFrame:
    with open(json_file_path, "r") as json_file:
        df: DataFrame = json_normalize(json.load(json_file))

        for col in Column.bad_fields():
            df.drop(col, 1, inplace=True)

        df.columns = [Column.translate(col) for col in df.columns]
        return df
