from sqlalchemy import Column, String, Integer, Text, Date
from sqlalchemy.orm import Mapped
from .base import Base, strLength


class StoreBookSQL(Base):
    __tablename__ = "storebook"

    _id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    store_id: Mapped[str] = Column(String(strLength))
    book_id: Mapped[str] = Column(String(strLength), nullable=False)
    stock_level: Mapped[int] = Column(Integer, nullable=False)
