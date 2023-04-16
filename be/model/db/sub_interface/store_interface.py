from ..db_client import DBClient
from pymongo.collection import Collection
from ...template.store_template import StoreBookTmp, StoreTemp
from ... import error
from typing import List, Dict, Any, Optional

class StoreInterface:
    def __init__(self, conn:DBClient):
        self.storeCol:Collection = conn.storeCol
        self.bookInfoCol:Collection = conn.bookInfoCol

    def book_id_exist(self, store_id, book_id) -> bool:
        cursor = self.storeCol.find_one(
            {"store_id": store_id, "book_list.book_id": book_id}
        )
        return cursor is not None
    
    def store_id_exist(self, store_id) -> bool:
        cursor = self.storeCol.find_one({"store_id": store_id})
        return cursor is not None
    
    def find_book(self, store_id:str, book_id:str) -> Optional[StoreBookTmp]:
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
        
    def get_book_info(self, book_info_id:str) -> Dict[str, Any]:
        doc = self.bookInfoCol.find_one({"_id": book_info_id})
        if doc is None:
            return None
        else:
            return doc["book_info"]
        
    def add_book_stock_level(self,store_id:str,book_id:str,count:int) -> int:
        result = self.storeCol.update_one(
            {
                "store_id": store_id,
                "book_list.book_id": book_id,
                "book_list.stock_level": {"$gte": -count},
            },
            {"$inc": {"book_list.$.stock_level": count}},
        )
        return result.modified_count
    
    def get_store_seller_id(self,store_id:str) -> Optional[str]:
        result = self.storeCol.find_one(
            {"store_id": store_id}, {"_id": 0, "user_id": 1}
        )
        if result is None:
            return None
        else:
            return result["user_id"]