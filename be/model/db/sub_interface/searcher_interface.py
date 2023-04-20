from typing import List, Dict, Any, Optional
from ...template.book_info import BookInfoTemp


class SearcherInterface:
    def __init__(self) -> None:
        pass

    def get_book_with_id(self, book_id: str) -> BookInfoTemp:
        """
        This function will return the full information of a book
        """
        pass

    def get_one_info_of_book(self, book_id: str, dictName: str):
        """
        This function will return a single information of one specific book
        """
        pass

    def find_book_with_one_dict(self, dictName: str, value) -> List[str]:
        """
        This function will return a book_id with book[dictName]=value
        This function would not search by book_id
        """
        pass

    def find_book_with_content(self, content_piece: str) -> List[str]:
        """
        This function returns a book_id which have a part of content_piece
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
