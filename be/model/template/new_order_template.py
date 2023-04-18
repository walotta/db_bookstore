from typing import Union, Dict, List


class NewOrderBookItemTemp:
    def __init__(self, book_id: str, count: int, price: int):
        self.book_id: str = book_id
        self.count: int = count
        self.price: int = price

    def to_dict(self) -> Dict[str, Union[str, int]]:
        return {"book_id": self.book_id, "count": self.count, "price": self.price}

    @staticmethod
    def from_dict(data: dict) -> "NewOrderBookItemTemp":
        return NewOrderBookItemTemp(data["book_id"], data["count"], data["price"])


class NewOrderTemp:
    def __init__(
        self,
        order_id: str,
        user_id: str,
        store_id: str,
        book_list: List[NewOrderBookItemTemp],
    ):
        self.order_id: str = order_id
        self.user_id: str = user_id
        self.store_id: str = store_id
        self.book_list: List[NewOrderBookItemTemp] = book_list

    def to_dict(self) -> Dict[str, Union[str, int, List[Dict[str, Union[str, int]]]]]:
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "store_id": self.store_id,
            "book_list": [book_item.to_dict() for book_item in self.book_list],
        }

    @staticmethod
    def from_dict(data: dict) -> "NewOrderTemp":
        return NewOrderTemp(
            data["order_id"],
            data["user_id"],
            data["store_id"],
            [
                NewOrderBookItemTemp.from_dict(book_item)
                for book_item in data["book_list"]
            ],
        )
