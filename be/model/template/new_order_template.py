from typing import Union, Dict


class NewOrderTemp:
    def __init__(
        self, order_id: str, store_id: str, book_id: str, count: int, price: int
    ):
        self.order_id: str = order_id
        self.store_id: str = store_id
        self.book_id: str = book_id
        self.count: int = count
        self.price: int = price

    def to_dict(self) -> Dict[str, Union[str, int]]:
        return {
            "order_id": self.order_id,
            "store_id": self.store_id,
            "book_id": self.book_id,
            "count": self.count,
            "price": self.price,
        }

    @staticmethod
    def from_dict(data: dict) -> "NewOrderTemp":
        return NewOrderTemp(
            data["order_id"],
            data["store_id"],
            data["book_id"],
            data["count"],
            data["price"],
        )
