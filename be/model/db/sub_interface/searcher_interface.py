from typing import List, Dict, Any, Optional, Union, Tuple
from pymongo.collection import Collection
from ...template.book_info import BookInfoTemp
from ..db_client import DBClient


# todo: These functions


class SearcherInterface:
    def __init__(self, conn: DBClient):
        self.storeCol: Collection = conn.storeCol
        self.bookInfoCol: Collection = conn.bookInfoCol

    def get_one_info_by_info_id(
        self, info_id: str, dictName: str
    ) -> Optional[Union[str, int, List[str]]]:
        """
        This function will return a single information of match info_id
        """
        result = self.bookInfoCol.find_one({"_id": info_id}, {"_id": 0, dictName: 1})
        print(result)
        if result is None:
            return None
        else:
            return result[dictName]

    def get_one_info_of_book(
        self, store_id: str, book_id: str, dictName: str
    ) -> Optional[Union[str, int, List[str]]]:
        """
        This function will return a single information of one specific book
        """
        pass

    def find_book_with_one_dict(self, dictName: str, value) -> List[Tuple[str, str]]:
        """
        This function will return a book_id with book[dictName]=value
        This function would not search by book_id
        """
        pass

    def find_book_with_content(self, content_piece: str) -> List[Tuple[str, str]]:
        """
        This function returns a book_id which have a part of content_piece
        """
        pass

    def find_book_with_tag(self, tags: List[str]) -> List[Tuple[str, str]]:
        """
        This function returns a book_id which have a tag
        """
        pass

    def find_book_in_one_store(self, store_id: str, dictName: str, value) -> List[str]:
        """
        This function will return a book_id which only in one store with book[dictName]=value
        """
        pass

    def find_book_in_one_store_with_content(
        self, store_id: str, content_piece: str
    ) -> List[str]:
        """
        This function will return a book_id which only in one store with book[dictName]=value
        """
        pass

    def find_book_in_one_store_with_tag(
        self, store_id: str, tags: List[str]
    ) -> List[str]:
        """
        This function will return a book_id which only in one store with book[dictName]=value
        """
        pass
