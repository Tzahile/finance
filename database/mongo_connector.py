from pymodm.connection import connect

from utils.configuration import Configurations


class BaseMongo:
    def __init__(self, connection_details: Configurations) -> None:
        connect(connection_details.mongo.get("URI"), alias=connection_details.mongo.get("ALIAS", "default"))
