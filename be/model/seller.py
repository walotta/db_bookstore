from pymongo.errors import PyMongoError
from . import error
from .db.interface import DBInterface
from .template.store_template import StoreBookTmp, StoreTemp
from typing import List, Tuple


class Seller():
    def __init__(self):
        self.db:DBInterface = DBInterface()

    def add_book(
        self,
        user_id: str,
        store_id: str,
        book_id: str,
        book_json_str: str,
        stock_level: int,
    ):
        try:
            if not self.db.user.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.db.store.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if self.db.store.book_id_exist(store_id, book_id):
                return error.error_exist_book_id(book_id)

            self.db.store.insert_one_book(
                store_id=store_id,
                book_id=book_id,
                book_info=book_json_str,
                stock_level=stock_level,
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
            if not self.db.user.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.db.store.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if not self.db.store.book_id_exist(store_id, book_id):
                return error.error_non_exist_book_id(book_id)

            self.db.store.add_book_stock_level(
                store_id=store_id, book_id=book_id, count=add_stock_level
            )
        except PyMongoError as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def create_store(self, user_id: str, store_id: str) -> Tuple[int, str]:
        try:
            if not self.db.user.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if self.db.store.store_id_exist(store_id):
                return error.error_exist_store_id(store_id)

            new_store = StoreTemp(store_id=store_id, user_id=user_id)
            self.db.store.insert_one_store(new_store)
        except PyMongoError as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"
