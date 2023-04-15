import uuid
import json
import logging
from pymongo.errors import PyMongoError
from . import db_conn
from . import error
from typing import List, Tuple, Dict, Any
from .template.new_order_template import NewOrderTemp
from .template.store_template import StoreBookTmp
from .template.user_template import UserTemp


class Buyer(db_conn.DBConn):
    def __init__(self):
        db_conn.DBConn.__init__(self)

    def new_order(
        self, user_id: str, store_id: str, id_and_count: List[Tuple[str, int]]
    ) -> Tuple[int, str, str]:
        order_id = ""
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id) + (order_id,)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id) + (order_id,)
            uid = "{}_{}_{}".format(user_id, store_id, str(uuid.uuid1()))

            for book_id, count in id_and_count:
                pipeline: List[Dict[str, Any]] = [
                    {"$match": {"store_id": store_id}},
                    {"$unwind": "$book_list"},
                    {"$match": {"book_list.book_id": book_id}},
                    {"$replaceRoot": {"newRoot": "$book_list"}},
                ]
                results = self.conn.storeCol.aggregate(pipeline=pipeline)
                doc = next(results, None)
                if doc is None:
                    return error.error_non_exist_book_id(book_id) + (order_id,)
                match_book = StoreBookTmp.from_dict(doc)

                stock_level = match_book.stock_level
                book_info = match_book.book_info
                book_info_json = json.loads(book_info)
                price = book_info_json.get("price")

                if stock_level < count:
                    return error.error_stock_level_low(book_id) + (order_id,)

                result = self.conn.storeCol.update_one(
                    {
                        "store_id": store_id,
                        "book_list.book_id": book_id,
                        "book_list.stock_level": {"$gte": count},
                    },
                    {"$inc": {"book_list.$.stock_level": -count}},
                )
                if result.modified_count == 0:
                    return error.error_stock_level_low(book_id) + (order_id,)

                new_order = NewOrderTemp(
                    order_id=uid,
                    user_id=user_id,
                    store_id=store_id,
                    book_id=book_id,
                    count=count,
                    price=price,
                )
                self.conn.newOrderCol.insert_one(new_order.to_dict())

            order_id = uid
        except PyMongoError as e:
            logging.info("528, {}".format(str(e)))
            return 528, "{}".format(str(e)), ""
        except BaseException as e:
            logging.info("530, {}".format(str(e)))
            return 530, "{}".format(str(e)), ""

        return 200, "ok", order_id

    def payment(self, user_id: str, password: str, order_id: str) -> Tuple[int, str]:
        conn = self.conn
        try:
            result = self.conn.newOrderCol.find_one({"order_id": order_id})
            if result is None:
                return error.error_invalid_order_id(order_id)
            match_order = NewOrderTemp.from_dict(result)

            order_id = match_order.order_id
            buyer_id = match_order.user_id
            store_id = match_order.store_id

            if buyer_id != user_id:
                return error.error_authorization_fail()

            result = self.conn.userCol.find_one({"user_id": user_id})
            if result is None:
                return error.error_non_exist_user_id(buyer_id)
            match_user = UserTemp.from_dict(result)
            balance = match_user.balance
            if password != match_user.password:
                return error.error_authorization_fail()

            result = self.conn.storeCol.find_one(
                {"store_id": store_id}, {"_id": 0, "user_id": 1}
            )
            if result is None:
                return error.error_non_exist_store_id(store_id)

            seller_id = result["user_id"]

            if not self.user_id_exist(seller_id):
                return error.error_non_exist_user_id(seller_id)

            results = self.conn.newOrderCol.find({"order_id": order_id})
            total_price = 0
            for row in results:
                tmp_order = NewOrderTemp.from_dict(row)
                count = tmp_order.count
                price = tmp_order.price
                total_price = total_price + price * count

            if balance < total_price:
                return error.error_not_sufficient_funds(order_id)

            result = self.conn.userCol.update_one(
                {"user_id": buyer_id, "balance": {"$gte": total_price}},
                {"$inc": {"balance": -total_price}},
            )
            if result.modified_count == 0:
                return error.error_not_sufficient_funds(order_id)

            result = self.conn.userCol.update_one(
                {"user_id": seller_id}, {"$inc": {"balance": total_price}}
            )

            if result.modified_count == 0:
                return error.error_non_exist_user_id(seller_id)

            result = self.conn.newOrderCol.delete_one({"order_id": order_id})
            if result.deleted_count == 0:
                return error.error_invalid_order_id(order_id)

        except PyMongoError as e:
            return 528, "{}".format(str(e))

        except BaseException as e:
            return 530, "{}".format(str(e))

        return 200, "ok"

    def add_funds(self, user_id, password, add_value) -> Tuple[int, str]:
        try:
            result = self.conn.userCol.find_one(
                {"user_id": user_id}, {"_id": 0, "password": 1}
            )
            if result is None:
                return error.error_authorization_fail()

            if result["password"] != password:
                return error.error_authorization_fail()

            result = self.conn.userCol.update_one(
                {"user_id": user_id}, {"$inc": {"balance": add_value}}
            )
            if result.modified_count == 0:
                return error.error_non_exist_user_id(user_id)

        except PyMongoError as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))

        return 200, "ok"
