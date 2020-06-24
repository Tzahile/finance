from typing import Dict

from pymodm.connection import connect


class BaseMongo:
    def __init__(self, config: Dict) -> None:
        connect(config.get("MONGO", {}).get("URI"), alias=config.get("MONGO", {}).get("ALIAS", "default"))
