from . import error
from typing import List, Dict, Any, Optional, Tuple
from .template.book_info import BookInfoTemp
from .db.interface import DBInterface


class Searcher:
    def __init__(self) -> None:
        self.db: DBInterface = DBInterface()

    def find_book_with_one_dict(
        self, dictName: str, value, page: int, store_id: Optional[str] = None
    ) -> Tuple[int, List[Tuple[str, str]]]:
        """
        Tuple[str,str] means (store_id, title)
        """
        st = (page - 1) * 20 + 1
        ed = page * 20
        return_dict = ["store_id", "title"]
        number = self.db.searcher.find_book_with_one_dict_n(dictName, value, store_id)
        return_list = self.db.searcher.find_book_with_one_dict(
            dictName, value, st, ed, return_dict, store_id
        )
        total_page = (number + 19) // 20 - 1
        return total_page, [(i["store_id"], i["title"]) for i in return_list]

    def find_book_with_content(
        self, content_piece: str, page: int, store_id: Optional[str] = None
    ) -> Tuple[int, List[Tuple[str, str]]]:
        st = (page - 1) * 20 + 1
        ed = page * 20
        return_dict = ["store_id", "title"]
        number = self.db.searcher.find_book_with_content_n(content_piece, store_id)
        return_list = self.db.searcher.find_book_with_content(
            content_piece, st, ed, return_dict, store_id
        )
        total_page = (number + 19) // 20 - 1
        return total_page, [(i["store_id"], i["title"]) for i in return_list]

    def find_book_with_tag(
        self, tags: List[str], page: int, store_id: Optional[str] = None
    ) -> Tuple[int, List[Tuple[str, str]]]:
        st = (page - 1) * 20 + 1
        ed = page * 20
        return_dict = ["store_id", "title"]
        number = self.db.searcher.find_book_with_tag_n(tags, store_id)
        return_list, number = self.db.searcher.find_book_with_tag(
            tags, st, ed, return_dict, store_id
        )
        total_page = (number + 19) // 20 - 1
        return total_page, [(i["store_id"], i["title"]) for i in return_list]
