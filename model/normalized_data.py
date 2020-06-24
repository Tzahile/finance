from __future__ import annotations

from pymodm import MongoModel, fields

from utils.configuration import config


class NormalizedData(MongoModel):
    id = fields.CharField()
    user_id = fields.ObjectIdField(required=True)
    date = fields.DateTimeField(blank=True)
    paper_num = fields.CharField(blank=True)
    transaction_num = fields.CharField(blank=True)
    paper = fields.CharField(blank=True)
    transaction = fields.CharField(blank=True)
    quantity = fields.IntegerField(blank=True)
    action = fields.CharField(blank=True)
    cash_balance = fields.FloatField(blank=True)
    commission = fields.FloatField(blank=True)
    cost = fields.FloatField(blank=True)

    def to_model(self) -> NormalizedData:
        odm_dict = self.to_son()
        odm_dict["id"] = str(odm_dict.pop("_id"))
        del odm_dict["_cls"]
        return NormalizedData(**odm_dict)

    class Meta:
        connection_alias = config.get("MONGO").get("ALIAS", "default")
