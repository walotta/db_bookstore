from pymongo.errors import PyMongoError
from . import error
from .db import db_conn
from .template.store_template import StoreBookTmp, StoreTemp
from typing import List, Tuple


class Seller(db_conn.DBConn):
    def __init__(self):
        db_conn.DBConn.__init__(self)

    def add_book(
        self,
        user_id: str,
        store_id: str,
        book_id: str,
        book_json_str: str,
        stock_level: int,
    ):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if self.book_id_exist(store_id, book_id):
                return error.error_exist_book_id(book_id)

            result = self.conn.bookInfoCol.insert_one({"book_info": book_json_str})
            info_id = result.inserted_id
            new_book = StoreBookTmp(
                book_id=book_id, book_info_id=info_id, stock_level=stock_level
            )
            self.conn.storeCol.update_one(
                {"store_id": store_id}, {"$push": {"book_list": new_book.to_dict()}}
            )
        except PyMongoError as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def add_stock_level(
        self, user_id: str, store_id: str, book_id: str, add_stock_level: int
    ):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if not self.book_id_exist(store_id, book_id):
                return error.error_non_exist_book_id(book_id)

            self.conn.storeCol.update_one(
                {"store_id": store_id, "book_list.book_id": book_id},
                {"$inc": {"book_list.$.stock_level": add_stock_level}},
            )
        except PyMongoError as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def create_store(self, user_id: str, store_id: str) -> Tuple[int, str]:
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if self.store_id_exist(store_id):
                return error.error_exist_store_id(store_id)

            new_store = StoreTemp(store_id=store_id, user_id=user_id)
            self.conn.storeCol.insert_one(new_store.to_dict())
        except PyMongoError as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"
