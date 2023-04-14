from typing import Dict, List, Union


class StoreBookTmp:
    def __init__(self, book_id: str, book_info: str, stock_level: int):
        self.book_id: str = book_id
        self.book_info: str = book_info
        self.stock_level: int = stock_level

    def to_dict(self) -> Dict[str, Union[str, int]]:
        return {
            "book_id": self.book_id,
            "book_info": self.book_info,
            "stock_level": self.stock_level,
        }

    @staticmethod
    def from_dict(data: dict) -> "StoreBookTmp":
        return StoreBookTmp(data["book_id"], data["book_info"], data["stock_level"])


class StoreTemp:
    def __init__(
        self,
        store_id: str,
        user_id: str,
        book_list: List[StoreBookTmp] = [],
        order_id_list: List[str] = [],
    ):
        self.store_id: str = store_id
        self.user_id: str = user_id
        self.book_list: List[StoreBookTmp] = book_list
        self.order_id_list: List[str] = order_id_list

    def to_dict(self) -> dict:
        return {
            "store_id": self.store_id,
            "user_id": self.user_id,
            "book_list": [book.to_dict() for book in self.book_list],
            "order_id_list": self.order_id_list,
        }

    @staticmethod
    def from_dict(data: dict) -> "StoreTemp":
        return StoreTemp(
            data["store_id"],
            data["user_id"],
            [StoreBookTmp.from_dict(book) for book in data["book_list"]],
            data["order_id_list"],
        )
