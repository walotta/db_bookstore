from sqlalchemy import Column, String, Integer, Text, Date, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from .base import Base, strLength


class OrderSQL(Base):
    __tablename__ = "order"

    _id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[str] = Column(String(strLength), nullable=False)
    user_id: Mapped[str] = Column(String(strLength), nullable=False)
    store_id: Mapped[str] = Column(String(strLength), nullable=False)
    book_id: Mapped[str] = Column(String(strLength), nullable=False)
    count: Mapped[int] = Column(Integer, nullable=False)
    price: Mapped[int] = Column(Integer, nullable=False)
    create_time: Mapped[int] = Column(Integer, nullable=False)
    status: Mapped[int] = Column(Integer, nullable=False)

    def __init__(
        self,
        order_id: str,
        user_id: str,
        store_id: str,
        book_id: str,
        count: int,
        price: int,
        create_time: int,
        status: int,
    ):
        self.order_id = order_id
        self.user_id = user_id
        self.store_id = store_id
        self.book_id = book_id
        self.count = count
        self.price = price
        self.create_time = create_time
        self.status = status

    def to_dict(self) -> dict:
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "store_id": self.store_id,
            "book_id": self.book_id,
            "count": self.count,
            "price": self.price,
            "create_time": self.create_time,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data: dict) -> "OrderSQL":
        return OrderSQL(
            data["order_id"],
            data["user_id"],
            data["store_id"],
            data["book_id"],
            data["count"],
            data["price"],
            data["create_time"],
            data["status"],
        )
