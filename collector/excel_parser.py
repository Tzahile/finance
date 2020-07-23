from typing import List, Dict
import pandas as pd


NAME_MAPPING = {
    "תאריך": "date",
    "נייר/תנועה": "paper_or_transaction",
    "מס' נייר/תנועה": "paper_id_or_transaction_id",
    "פעולה": "action",
    "כמות": "quantity",
    "מחיר": "cost",
    "זכות נטו": "net_credit",
    "חובה נטו": "net_owe",
    "עמלה": "commission",
    "יתרה": "cash_balance",
    "אסמכתא": "reference",
}


def parse_excel(excel_name: str) -> List[Dict]:
    raw_data = []
    dfs = pd.read_excel(excel_name, sheet_name=None)
    for _, df in dfs.items():
        df.rename(columns=NAME_MAPPING, inplace=True)
        data = df.to_dict(orient="records")
        raw_data.extend(data)
    return raw_data
