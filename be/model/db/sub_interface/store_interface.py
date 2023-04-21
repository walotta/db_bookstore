from ..db_client import DBClient
from pymongo.collection import Collection
from ...template.store_template import StoreBookTmp, StoreTemp
from ... import error
from typing import List, Dict, Any, Optional
from ...template.book_info import BookInfoTemp


class StoreInterface:
    def __init__(self, conn: DBClient):
        self.storeCol: Collection = conn.storeCol
        self.bookInfoCol: Collection = conn.bookInfoCol

    def book_id_exist(self, store_id, book_id) -> bool:
        cursor = self.storeCol.find_one(
            {"store_id": store_id, "book_list.book_id": book_id}
        )
        return cursor is not None

    def store_id_exist(self, store_id) -> bool:
        cursor = self.storeCol.find_one({"store_id": store_id})
        return cursor is not None

    def find_book(self, store_id: str, book_id: str) -> Optional[StoreBookTmp]:
        pipeline: List[Dict[str, Any]] = [
            {"$match": {"store_id": store_id}},
            {"$unwind": "$book_list"},
            {"$match": {"book_list.book_id": book_id}},
            {"$replaceRoot": {"newRoot": "$book_list"}},
        ]
        results = self.storeCol.aggregate(pipeline=pipeline)
        doc = next(results, None)
        if doc is None:
            return None
        else:
            return StoreBookTmp.from_dict(doc)

    def get_book_info(self, book_info_id: str) -> Optional[Dict[str, Any]]:
        doc = self.bookInfoCol.find_one({"_id": book_info_id})
        if doc is None:
            return None
        else:
            return doc["book_info"]

    def add_stock_level(self, store_id: str, book_id: str, count: int) -> int:
        result = self.storeCol.update_one(
            {"store_id": store_id},
            {"$inc": {"book_list.$[elem].stock_level": count}},
            array_filters=[
                {"elem.book_id": book_id, "elem.stock_level": {"$gte": min(0, -count)}}
            ],
        )
        return result.modified_count

    def get_store_seller_id(self, store_id: str) -> Optional[str]:
        result = self.storeCol.find_one(
            {"store_id": store_id}, {"_id": 0, "user_id": 1}
        )
        if result is None:
            return None
        else:
            return result["user_id"]

    def insert_one_book(
        self, store_id: str, book_id: str, stock_level: int, book_info: str
    ) -> None:
        new_book_info = BookInfoTemp(book_info, store_id)
        result = self.bookInfoCol.insert_one(new_book_info.to_dict())
        info_id = result.inserted_id
        new_book = StoreBookTmp(
            book_id=book_id, book_info_id=info_id, stock_level=stock_level
        )
        self.storeCol.update_one(
            {"store_id": store_id}, {"$push": {"book_list": new_book.to_dict()}}
        )

    def insert_one_store(self, new_store: StoreTemp) -> None:
        self.storeCol.insert_one(new_store.to_dict())
