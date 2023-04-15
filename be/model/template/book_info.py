

class BookInfoTemp:
    def __init__(self,book_info:str):
        self.book_info: str = book_info

    def to_dict(self) -> dict:
        return {
            "book_info": self.book_info,
        }
    
    @staticmethod
    def from_dict(data: dict) -> "BookInfoTemp":
        return BookInfoTemp(data["book_info"])