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

    def find_book_with_one_dict(
        self, dictName: str, value, st: int, ed: int, return_dict: List[str]
    ) -> Tuple[List[Dict[str,str]], int]:
        """
        This function could search books with one dict matching.
        Input:
            dict_name:  str
            value:      str/int
            st:         int
            ed:         int
            return_dict List[str]

        Output:
            List[List[return_items]]
            book_number

        The st and ed normally satisfy ed-st+1=20, and it will be 1-base
        Nomally we would require 'store_id' and 'book_id' and 'title' in return_dict
        The function returns some books with book[dictName]=value
        This function would not search by book_id
        """
        pass

    def find_book_with_content(
        self, content_piece: str, st: int, ed: int, return_dict: List[str]
    ) -> Tuple[List[Dict[str,str]], int]:
        """
        This function returns a book_id which have a part of content_piece
        """
        pass

    def find_book_with_tag(
        self, tags: List[str], st: int, ed: int, return_dict: List[str]
    ) -> Tuple[List[Dict[str,str]], int]:
        """
        This function returns a book_id which have a tag
        """
        pass

    def find_book_in_one_store(
        self,
        store_id: str,
        dictName: str,
        value,
        st: int,
        ed: int,
        return_dict: List[str],
    ) -> Tuple[List[Dict[str,str]], int]:
        """
        This function will return a book_id which only in one store with book[dictName]=value
        """
        pass

    def find_book_in_one_store_with_content(
        self,
        store_id: str,
        content_piece: str,
        st: int,
        ed: int,
        return_dict: List[str],
    ) -> Tuple[List[Dict[str,str]], int]:
        """
        This function will return a book_id which only in one store with book[dictName]=value
        """
        pass

    def find_book_in_one_store_with_tag(
        self, store_id: str, tags: List[str], st: int, ed: int, return_dict: List[str]
    ) -> Tuple[List[Dict[str,str]], int]:
        """
        This function will return a book_id which only in one store with book[dictName]=value
        """
        pass