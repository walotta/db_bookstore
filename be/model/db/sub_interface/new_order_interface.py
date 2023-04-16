from ..db_client import DBClient
from pymongo.collection import Collection
from ...template.new_order_template import NewOrderTemp, NewOrderBookItemTemp
from typing import Optional

class NewOrderInterface:
    def __init__(self, conn:DBClient):
        self.newOrderCol:Collection = conn.newOrderCol

    def insert_new_order(self, new_order:NewOrderTemp):
        self.newOrderCol.insert_one(new_order.to_dict())

    def find_new_order(self, order_id:str) -> Optional[NewOrderTemp]:
        doc = self.newOrderCol.find_one({"order_id": order_id})
        if doc is None:
            return None
        else:
            return NewOrderTemp.from_dict(doc)
        
    def delete_order(self, order_id:str) -> int:
        result = self.newOrderCol.delete_one({"order_id": order_id})
        return result.deleted_count