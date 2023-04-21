import pytest

from fe.test.gen_book_data import GenBook
from fe.access.new_buyer import register_new_buyer
from fe.access.new_seller import register_new_seller
from fe.access.book import Book
import uuid
import random


class TestOrderFunctions:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seller_id = "test_order_functions_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_order_functions_store_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_order_functions_buyer_id_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id
        b = register_new_buyer(self.buyer_id, self.password)
        self.buyer = b
        self.order_num = 12
        self.order_id_list = []
        self.price_list = []
        self.buy_book_id_list_list = []
        self.status_list = []
        self.gen_book_list = []

        def new_order(i):
            gen_book = GenBook(self.seller_id + str(i), self.store_id + str(i))
            self.gen_book_list.append(gen_book)
            gen_book.buy_book_info_list.clear()
            ok, buy_book_id_list = gen_book.gen(
                non_exist_book_id=False, low_stock_level=False, max_book_count=5
            )
            buy_book_info_list = gen_book.buy_book_info_list
            assert ok
            self.buy_book_id_list_list.append(buy_book_id_list)
            code, order_id = b.new_order(self.store_id + str(i), buy_book_id_list)
            assert code == 200
            total_price = 0
            for item in buy_book_info_list:
                book: Book = item[0]
                num = item[1]
                if book.price is None:
                    continue
                else:
                    total_price = total_price + book.price * num
            return order_id, total_price

        for i in range(self.order_num):
            order_id, total_price = new_order(i)
            self.order_id_list.append(order_id)
            self.price_list.append(total_price)
        yield

    def test_query_order(self):
        for i in range(self.order_num):
            order_id = self.order_id_list[i]
            total_price = self.price_list[i]
            status = random.randint(0, 3)
            self.status_list.append(status)
            if status == 0:
                continue
            code = self.buyer.add_funds(total_price)
            assert code == 200
            code = self.buyer.payment(order_id)
            assert code == 200
            if status == 1:
                continue
            code = self.gen_book_list[i].seller.ship_order(order_id)
            assert code == 200
            if status == 2:
                continue
            code = self.buyer.receive_order(order_id)
            assert code == 200
        code, order_id_list = self.buyer.query_order_id_list()
        assert code == 200
        assert order_id_list == self.order_id_list
        order_list = [self.buyer.query_order(order_id)[1] for order_id in order_id_list]
        for i in range(self.order_num):
            order = order_list[i]
            assert order["order_id"] == self.order_id_list[i]
            assert order["user_id"] == self.buyer_id
            assert order["store_id"] == self.store_id + str(i)
            assert order["status"] == self.status_list[i]
            tot_price = 0
            for book in order["book_list"]:
                assert book["book_id"] in [j[0] for j in self.buy_book_id_list_list[i]]
                tot_price = tot_price + book["price"] * book["count"]
            assert tot_price == self.price_list[i]
