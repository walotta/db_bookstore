import pymongo
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Any


class DBClient:
    def __init__(self, connectUrl="mongodb://localhost:27017/", database="bookstore"):
        self.connectUrl: str = connectUrl
        self.database: str = database
        self.client: MongoClient = pymongo.MongoClient(connectUrl)

    def database_init(self) -> None:
        self.db: Database = self.client[self.database]
        self.userCol: Collection[Any] = self.db["user"]
        self.userCol.create_index("user_id", unique=True)
        self.storeCol: Collection[Any] = self.db["store"]
        self.storeCol.create_index("store_id", unique=True)
        self.bookCol: Collection[Any] = self.db["book"]
        self.bookCol.create_index("book_id", unique=True)
        self.newOrderCol: Collection[Any] = self.db["new_order"]
        self.newOrderCol.create_index("order_id", unique=True)

    def database_reset(self) -> None:
        self.client.drop_database(self.database)
        self.database_init()
