from typing import Optional, List, Dict, Union


class UserTemp:
    def __init__(
        self,
        user_id: str,
        password: str,
        balance: int,
        token: str,
        terminal: str,
    ):
        self.user_id: str = user_id
        self.password: str = password
        self.balance: int = balance
        self.token: str = token
        self.terminal: str = terminal

    def to_dict(self) -> Dict[str, Union[str, int, List[str], Optional[str]]]:
        return {
            "user_id": self.user_id,
            "password": self.password,
            "balance": self.balance,
            "token": self.token,
            "terminal": self.terminal,
        }

    @staticmethod
    def from_dict(data: dict) -> "UserTemp":
        return UserTemp(
            data["user_id"],
            data["password"],
            data["balance"],
            data["token"],
            data["terminal"],
        )
