from sqlalchemy import Column, String, Integer, Text, Date
from sqlalchemy.orm import Mapped
from .base import Base, strLength


class StoreSQL(Base):
    __tablename__ = "store"

    store_id: Mapped[str] = Column(String(strLength), primary_key=True)
    user_id: Mapped[str] = Column(String(strLength), nullable=False)

    def __init__(self, store_id: str, user_id: str):
        self.store_id = store_id
        self.user_id = user_id

    def to_dict(self) -> dict:
        return {
            "store_id": self.store_id,
            "user_id": self.user_id,
        }

    @staticmethod
    def from_dict(data: dict) -> "StoreSQL":
        return StoreSQL(
            data["store_id"],
            data["user_id"],
        )
