from typing import Optional, List, Dict, Union


class UserTemp:
    def __init__(
        self,
        user_id: str,
        password: str,
        balance: int,
        token: str,
        terminal: str,
        store_id_list: List[str] = [],
    ):
        self.user_id: str = user_id
        self.password: str = password
        self.balance: int = balance
        self.token: str = token
        self.terminal: str = terminal
        self.store_id_list: List[str] = store_id_list

    def to_dict(self) -> Dict[str, Union[str, int, List[str], Optional[str]]]:
        return {
            "user_id": self.user_id,
            "password": self.password,
            "balance": self.balance,
            "store_id_list": self.store_id_list,
            "token": self.token,
            "terminal": self.terminal,
        }

    @staticmethod
    def from_dict(data: dict) -> "UserTemp":
        return UserTemp(
            data["user_id"],
            data["password"],
            data["balance"],
            data["store_id_list"],
            data["token"],
            data["terminal"],
        )
