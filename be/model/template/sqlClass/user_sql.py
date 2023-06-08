from sqlalchemy import Column, String, Integer, Text, Date
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from .base import Base, strLength, longStrLength


class UserSQL(Base):
    __tablename__ = "user"

    user_id: Mapped[str] = Column(String(strLength), primary_key=True)
    password: Mapped[str] = Column(String(strLength), nullable=False)
    balance: Mapped[int] = Column(Integer, nullable=False)
    token: Mapped[str] = Column(String(longStrLength), nullable=False)
    terminal: Mapped[str] = Column(String(strLength), nullable=False)

    def __init__(
        self, user_id: str, password: str, balance: int, token: str, terminal: str
    ):
        self.user_id = user_id
        self.password = password
        self.balance = balance
        self.token = token
        self.terminal = terminal

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "password": self.password,
            "balance": self.balance,
            "token": self.token,
            "terminal": self.terminal,
        }

    @staticmethod
    def from_dict(data: dict) -> "UserSQL":
        return UserSQL(
            data["user_id"],
            data["password"],
            data["balance"],
            data["token"],
            data["terminal"],
        )
