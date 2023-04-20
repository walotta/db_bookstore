class BookInfoTemp:
    def __init__(self, book_info: str):
        temp_dict = eval(book_info)
        for key in temp_dict:
            setattr(self, key, temp_dict[key])
        self.book_id = temp_dict["id"]

    def to_dict(self) -> dict:
        return self.__dict__

    @staticmethod
    def from_dict(data: dict) -> "BookInfoTemp":
        return BookInfoTemp(str(data))

    # The name of the variables:
    #   book_id: str
    #   id: str
    #   title: str
    #   author: str
    #   publisher: str
    #   original_title: str
    #   translator: str
    #   pub_year: str
    #   pages: int
    #   price: int
    #   currency_unit: int
    #   binding: str
    #   isbn: str
    #   author_intro: str
    #   book_intro: str
    #   content: str
    #   tags: List[str]
    #   pictures: List[str]
