import pytest

from fe.test.gen_book_data import GenBook
from fe.access.searcher import Searcher
from fe.access import book
from fe import conf
import uuid, random

from fe.bench.workload import Workload
from fe.access.new_seller import register_new_seller
from fe.access.seller import Seller
from typing import List, Tuple


class TestSearchBook:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        # wl = Workload()
        # wl.gen_database()

        self.searcher = Searcher(conf.URL)

        # seller process
        self.seller_number = 5
        self.seller_list: List[Seller] = []
        self.seller_id_list = []
        for i in range(1, self.seller_number + 1):
            new_seller_id = "test_add_books_seller_id_{}".format(str(uuid.uuid1()))
            new_seller = register_new_seller(new_seller_id, self.password)
            self.seller_list.append(new_seller)
            self.seller_id_list.append(new_seller_id)

        # generate books
        self.book_db = book.BookDB()
        rows = self.book_db.get_book_count()
        start = 0
        max_book_count = 1000
        if rows > max_book_count:
            start = random.randint(0, rows - max_book_count)
        size = random.randint(1, max_book_count)
        self.books = self.book_db.get_book_info(start, size)

        # put books into sellers
        for bk in range(self.books):
            cu_seller = self.seller_list[bk % self.seller_number]
            code = cu_seller.add_book(cu_seller.seller_id, 0, bk)
            assert code == 200

        yield

    def test_search_with_title(self):
        for i in self.books:
            target_title = i.title
            # get answer from self.books
            answer_list: List[str] = []  # only store_id list
            for j in range(self.books):
                if self.books[j].title == target_title:
                    answer_list.append(self.seller_id_list[j % self.seller_number])

            # get our answer for request
            cu_page = 0
            total_page = 1
            check_list = []
            while cu_page <= total_page:
                cu_page = cu_page + 1
                code, cu_page, total_page, temp_list = self.searcher.find_book(
                    "one_dict", "title", target_title, None, cu_page
                )
                assert code == 200
                for k in temp_list:
                    # filter for data generate by other test
                    if k[0] in self.seller_id_list:
                        check_list.append(k[0])

            # compare answer_list and check_list
            ans = set(answer_list)
            chk = set(check_list)
            assert ans == chk

    def test_search_with_author(self):
        for i in self.books:
            target_author = i.author
            # get answer from self.books
            answer_list: List[Tuple[str, str]] = []  # only store_id list
            for j in range(self.books):
                if self.books[j].author == target_author:
                    answer_list.append(
                        (
                            self.seller_id_list[j % self.seller_number],
                            self.books[j].title,
                        )
                    )

            # get our answer for request
            cu_page = 0
            total_page = 1
            check_list: List[Tuple[str, str]] = []
            while cu_page <= total_page:
                cu_page = cu_page + 1
                code, cu_page, total_page, temp_list = self.searcher.find_book(
                    "one_dict", "author", target_author, None, cu_page
                )
                assert code == 200
                for k in temp_list:
                    # filter for data generate by other test
                    if k[1] in self.seller_id_list:
                        check_list.append(k)

            # compare answer_list and check_list
            ans = set(answer_list)
            chk = set(check_list)
            assert ans == chk

    def test_search_with_tags(self):
        for i in self.books:
            if len(i.tags) > 1:
                target_tags = i.tags[:2]
            else:
                target_tags = i.tags
            # get answer from self.books
            answer_list: List[Tuple[str, str]] = []  # only store_id list
            for j in range(self.books):
                if set(target_tags) <= set(self.books[j].tags):
                    answer_list.append(
                        (
                            self.seller_id_list[j % self.seller_number],
                            self.books[j].title,
                        )
                    )

            # get our answer for request
            cu_page = 0
            total_page = 1
            check_list: List[Tuple[str, str]] = []
            while cu_page <= total_page:
                cu_page = cu_page + 1
                code, cu_page, total_page, temp_list = self.searcher.find_book(
                    "tags", None, target_tags, None, cu_page
                )
                assert code == 200
                for k in temp_list:
                    # filter for data generate by other test
                    if k[1] in self.seller_id_list:
                        check_list.append(k)

            # compare answer_list and check_list
            ans = set(answer_list)
            chk = set(check_list)
            assert ans == chk

    def test_search_with_contents(self):
        for i in self.books:
            if len(i.content) > 1:
                start = random.randint(0, len(i.content))
                endd = random.randint(start, len(i.content))
                target_contents = i.content[start:endd]
            else:
                target_contents = i.content
            # get answer from self.books
            answer_list: List[Tuple[str, str]] = []  # only store_id list
            for j in range(self.books):
                if target_contents in self.books[j].content:
                    answer_list.append(
                        (
                            self.seller_id_list[j % self.seller_number],
                            self.books[j].title,
                        )
                    )

            # get our answer for request
            cu_page = 0
            total_page = 1
            check_list: List[Tuple[str, str]] = []
            while cu_page <= total_page:
                cu_page = cu_page + 1
                code, cu_page, total_page, temp_list = self.searcher.find_book(
                    "content", None, target_contents, None, cu_page
                )
                assert code == 200
                for k in temp_list:
                    # filter for data generate by other test
                    if k[1] in self.seller_id_list:
                        check_list.append(k)

            # compare answer_list and check_list
            ans = set(answer_list)
            chk = set(check_list)
            assert ans == chk

    def test_search_with_author_with_store_id(self):
        for i in self.books:
            target_author = i.author
            target_store_id = self.seller_id_list[i % self.seller_number]

            # get answer from self.books
            answer_list: List[Tuple[str, str]] = []  # only store_id list
            for j in range(self.books):
                if (
                    self.books[j].author == target_author
                    and i % self.seller_number == j % self.seller_number
                ):
                    answer_list.append(
                        (
                            self.seller_id_list[j % self.seller_number],
                            self.books[j].title,
                        )
                    )

            # get our answer for request
            cu_page = 0
            total_page = 1
            check_list: List[Tuple[str, str]] = []
            while cu_page <= total_page:
                cu_page = cu_page + 1
                code, cu_page, total_page, temp_list = self.searcher.find_book(
                    "one_dict", "author", target_author, target_store_id, cu_page
                )
                assert code == 200
                for k in temp_list:
                    # filter for data generate by other test
                    if k[1] in self.seller_id_list:
                        check_list.append(k)

            # compare answer_list and check_list
            ans = set(answer_list)
            chk = set(check_list)
            assert ans == chk
