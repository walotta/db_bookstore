from typing import Optional, List, Dict, Union


class UserTemp:
    def __init__(
        self,
        name: str,
        password: str,
        balabce: int,
        store_id_list: List[str] = [],
        token: Optional[str] = None,
        terminal: Optional[str] = None,
    ):
        self.name: str = name
        self.password: str = password
        self.balance: int = balabce
        self.store_id_list: List[str] = store_id_list
        self.token: Optional[str] = token
        self.terminal: Optional[str] = terminal

    def to_dict(self) -> Dict[str, Union[str, int, List[str], Optional[str]]]:
        return {
            "name": self.name,
            "password": self.password,
            "balance": self.balance,
            "store_id_list": self.store_id_list,
            "token": self.token,
            "terminal": self.terminal,
        }

    @staticmethod
    def from_dict(data: dict) -> "UserTemp":
        return UserTemp(
            data["name"],
            data["password"],
            data["balance"],
            data["store_id_list"],
            data["token"],
            data["terminal"],
        )
