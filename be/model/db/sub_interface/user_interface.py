from ..db_client import DBClient
from pymongo.collection import Collection
from ...template.user_template import UserTemp
from typing import Optional

class UserInterface:
    def __init__(self, conn:DBClient):
        self.userCol:Collection = conn.userCol

    def user_id_exist(self, user_id:str) -> bool:
        cursor = self.userCol.find_one({"user_id": user_id})
        return cursor is not None
    
    def find_user(self, user_id:str) -> Optional[UserTemp]:
        result = self.userCol.find_one({"user_id": user_id})
        if result is None:
            return None
        else:
            return UserTemp.from_dict(result)
        
    def add_balance(self, user_id:str, count:int) -> int:
        result = self.userCol.update_one(
            {"user_id": user_id, "balance": {"$gte": -count}},
            {"$inc": {"balance":count}},
        )
        return result.modified_count
    
    def get_password(self, user_id:str) -> Optional[str]:
        result = self.userCol.find_one(
                {"user_id": user_id}, {"_id": 0, "password": 1}
            )
        if result is None:
            return None
        else:
            return result["password"]
        
    def get_balance(self, user_id:str) -> Optional[int]:
        result = self.userCol.find_one(
                {"user_id": user_id}, {"_id": 0, "balance": 1}
            )
        if result is None:
            return None
        else:
            return result["balance"]