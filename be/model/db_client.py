import pymongo
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Any, Optional


class DBClient:
    def __init__(self, connectUrl="mongodb://localhost:27017/", database="bookstore"):
        self.connectUrl: str = connectUrl
        self.database: str = database
        self.client: MongoClient = pymongo.MongoClient(connectUrl)

    def database_init(self) -> None:
        self.db: Database = self.client[self.database]
        self.userCol: Collection[Any] = self.db["user"]
        self.userCol.create_index([("user_id", 1)], unique=True)
        self.storeCol: Collection[Any] = self.db["store"]
        self.storeCol.create_index(
            [("store_id", 1), ("book_list.book_id", 1)], unique=True
        )
        self.bookInfoCol: Collection[Any] = self.db["book_info"]
        self.newOrderCol: Collection[Any] = self.db["new_order"]
        self.newOrderCol.create_index([("order_id", 1), ("book_id", 1)], unique=True)

    def database_reset(self) -> None:
        self.client.drop_database(self.database)
        self.database_init()

    def database_close(self) -> None:
        self.client.close()


database_instance: Optional[DBClient] = None


def db_init() -> None:
    global database_instance
    database_instance = DBClient()
    database_instance.database_init()


def get_db_conn() -> DBClient:
    global database_instance
    assert database_instance is not None, "Database not initialized"
    return database_instance
