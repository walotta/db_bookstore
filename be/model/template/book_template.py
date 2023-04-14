from typing import Optional, Dict, Union


class BookTemp:
    def __init__(self, book_id: str, book_info: Optional[str] = None):
        self.book_id: str = book_id
        self.book_info: Optional[str] = book_info

    def to_dict(self) -> Dict[str, Union[str, Optional[str]]]:
        return {
            "book_id": self.book_id,
            "book_info": self.book_info,
        }

    @staticmethod
    def from_dict(data: dict) -> "BookTemp":
        return BookTemp(data["book_id"], data["book_info"])
