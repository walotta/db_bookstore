from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.orm import Mapped
from .base import Base, strLength


class BookInfoSQL(Base):
    __tablename__ = "bookinfo"

    # _id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    book_id: Mapped[str] = Column(String(strLength), primary_key=True)
    title: Mapped[str] = Column(String(strLength))
    author: Mapped[str] = Column(String(strLength))
    publisher: Mapped[str] = Column(String(strLength))
    original_title: Mapped[str] = Column(String(strLength))
    translator: Mapped[str] = Column(String(strLength))
    pub_year: Mapped[str] = Column(String(strLength))
    pages: Mapped[int] = Column(Integer)
    price: Mapped[int] = Column(Integer)
    currency_unit: Mapped[str] = Column(String(strLength))
    binding: Mapped[str] = Column(String(strLength))
    isbn: Mapped[str] = Column(String(strLength))
    author_intro: Mapped[str] = Column(Text)
    book_intro: Mapped[str] = Column(Text)
    content: Mapped[str] = Column(Text)

    def __init__(
        self,
        book_id: str,
        title: str,
        author: str,
        publisher: str,
        original_title: str,
        translator: str,
        pub_year: str,
        pages: str,
        price: str,
        currency_unit: int,
        binding: str,
        isbn: str,
        author_intro: str,
        book_intro: str,
        content: str,
    ):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.publisher = publisher
        self.original_title = original_title
        self.translator = translator
        self.pub_year = pub_year
        self.pages = pages
        self.price = price
        self.currency_unit = currency_unit
        self.binding = binding
        self.isbn = isbn
        self.author_intro = author_intro
        self.book_intro = book_intro
        self.content = content

    def to_dict(self) -> dict:
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "publisher": self.publisher,
            "original_title": self.original_title,
            "translator": self.translator,
            "pub_year": self.pub_year,
            "pages": self.pages,
            "price": self.price,
            "currency_unit": self.currency_unit,
            "binding": self.binding,
            "isbn": self.isbn,
            "author_intro": self.author_intro,
            "book_intro": self.book_intro,
            "content": self.content,
        }

    @staticmethod
    def from_dict(data: dict) -> "BookInfoSQL":
        return BookInfoSQL(
            data["book_id"],
            data["title"],
            data["author"],
            data["publisher"],
            data["original_title"],
            data["translator"],
            data["pub_year"],
            data["pages"],
            data["price"],
            data["currency_unit"],
            data["binding"],
            data["isbn"],
            data["author_intro"],
            data["book_intro"],
            data["content"],
        )
