from ..db_client import DBClient
from pymongo.collection import Collection
from ...template.new_order_template import NewOrderTemp, NewOrderBookItemTemp
from typing import Optional
from ...template.new_order_template import STATUS


class NewOrderInterface:
    def __init__(self, conn: DBClient):
        self.newOrderCol: Collection = conn.newOrderCol

    def insert_new_order(self, new_order: NewOrderTemp):
        self.newOrderCol.insert_one(new_order.to_dict())

    def find_new_order(self, order_id: str) -> Optional[NewOrderTemp]:
        doc = self.newOrderCol.find_one({"order_id": order_id})
        if doc is None:
            return None
        else:
            return NewOrderTemp.from_dict(doc)

    def delete_order(self, order_id: str) -> int:
        result = self.newOrderCol.delete_one({"order_id": order_id})
        return result.deleted_count

    def order_id_exist(self, order_id: str) -> bool:
        cursor = self.newOrderCol.find_one({"order_id": order_id})
        return cursor is not None

    def update_new_order_status(self, order_id: str, status: STATUS) -> int:
        result = self.newOrderCol.update_one({"order_id":order_id},{"$set":{"status":status.value}})
        return result.modified_count

    def find_order_status(self, order_id: str) -> Optional[STATUS]:
        result = self.newOrderCol.find_one({"order_id":order_id},{"_id":0,"status":1})
        if result is None:
            return None
        else:
            return STATUS(result["status"])
