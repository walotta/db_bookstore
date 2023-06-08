from sqlalchemy import Column, String, Integer, Text, Date
from sqlalchemy.orm import Mapped
from .base import Base, strLength


class BookInfoPicSQL(Base):
    __tablename__ = "bookinfopic"

    _id: Mapped[int] = Column(
        Integer, autoincrement=True, primary_key=True, unique=True, nullable=False
    )
    book_id: Mapped[str] = Column(String(strLength), nullable=False)
    pic: Mapped[str] = Column(Text, nullable=False)
