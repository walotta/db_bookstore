import pytest

from fe.test.gen_book_data import GenBook
from fe.access.new_buyer import register_new_buyer
from fe.access.new_seller import register_new_seller
import uuid


class TestOrderDeliver:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seller_id = "test_order_deliver_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_order_deliver_store_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_order_deliver_buyer_id_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id
        self.buyer = register_new_buyer(self.buyer_id, self.password)
        self.seller = register_new_seller(self.seller_id, self.password)
        self.gen_book = GenBook(self.seller_id, self.store_id)
        yield

    def test_deliver_order(self):
        ok, buy_book_id_list = self.gen_book.gen(
            non_exist_book_id=False, low_stock_level=False
        )
        assert ok
        code, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        assert code == 200
        code, _ = self.seller.ship_order(order_id)
        assert code == 200
        code, _ = self.buyer.receive_order(order_id)
        assert code == 200
