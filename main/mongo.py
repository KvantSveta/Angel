from pymongo import MongoClient


class Mongo:
    def __init__(
        self,
        db_name,
        collection_name,
        ip_address="localhost",
        port=27017,
        server_timeout_ms=1000
    ):

        self._client = MongoClient(
            host=ip_address,
            port=port,
            serverSelectionTimeoutMS=server_timeout_ms
        )

        self._db = self._client[db_name]

        self.collection = self._db[collection_name]
