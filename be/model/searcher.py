from . import error
from typing import List, Dict, Any, Optional, Tuple
from .template.book_info import BookInfoTemp
from .db.interface import DBInterface


# todo: we need to add some checking for correctness
class Searcher:
    def __init__(self) -> None:
        pass

    def find_book_with_one_dict(self, dictName: str, value) -> List[Tuple[str, str]]:
        """
        Tuple[str,str] means (store_id, book_id)
        """

        pass

    def find_book_with_content(self, content_piece: str) -> List[Tuple[str, str]]:
        pass

    def find_book_with_tag(self, tags: List[str]) -> List[Tuple[str, str]]:
        pass

    def find_book_in_one_store(self, store_id: str, dictName: str, value) -> List[str]:
        pass

    def find_book_in_one_store_with_content(
        self, store_id: str, content_piece: str
    ) -> List[str]:
        pass

    def find_book_in_one_store_with_tag(
        self, store_id: str, tags: List[str]
    ) -> List[str]:
        pass
