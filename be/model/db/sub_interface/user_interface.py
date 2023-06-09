from ..db_client import DBClient
from ...template.user_template import UserTemp
from ...template.sqlClass.user_sql import UserSQL
from ...template.sqlClass.order_sql import OrderSQL
from typing import Optional, List
from sqlalchemy.orm import Session


class UserInterface:
    def __init__(self):
        pass

    def user_id_exist(self, user_id: str, session: Session) -> bool:
        match_user = session.query(UserSQL).filter_by(user_id=user_id).first()
        return match_user is not None

    def add_balance(self, user_id: str, count: int, session: Session) -> int:
        match_user = session.query(UserSQL).filter_by(user_id=user_id).first()
        if match_user is None:
            return -1
        match_user.balance += count
        if match_user.balance < 0:
            return -1
        session.add(match_user)
        return 1

    def get_password(self, user_id: str, session: Session) -> Optional[str]:
        match_user = session.query(UserSQL).filter_by(user_id=user_id).first()
        if match_user is None:
            return None
        else:
            return match_user.password

    def get_balance(self, user_id: str, session: Session) -> Optional[int]:
        match_user = session.query(UserSQL).filter_by(user_id=user_id).first()
        if match_user is None:
            return None
        else:
            return match_user.balance

    def get_token(self, user_id: str, session: Session) -> Optional[str]:
        match_user = session.query(UserSQL).filter_by(user_id=user_id).first()
        if match_user is None:
            return None
        else:
            return match_user.token

    def insert_one_user(self, user: UserTemp, session: Session) -> None:
        assert len(user.order_id_list) == 0
        user_sql = UserSQL.from_dict(user.to_dict())
        session.add(user_sql)

    def update_token_terminal(
        self, user_id: str, token: str, terminal: str, session: Session
    ) -> int:
        match_user = session.query(UserSQL).filter_by(user_id=user_id).first()
        if match_user is None:
            return -1
        match_user.token = token
        match_user.terminal = terminal
        session.add(match_user)
        return 1

    def delete_user(self, user_id: str, session: Session) -> int:
        match_user = session.query(UserSQL).filter_by(user_id=user_id).first()
        if match_user is None:
            return -1
        session.delete(match_user)
        return 1

    def update_password(
        self, user_id: str, password: str, token: str, terminal: str, session: Session
    ) -> int:
        match_user = session.query(UserSQL).filter_by(user_id=user_id).first()
        if match_user is None:
            return -1
        match_user.password = password
        match_user.token = token
        match_user.terminal = terminal
        session.add(match_user)
        return 1

    def add_order(self, user_id: str, order_id: str, session: Session) -> int:
        if self.user_id_exist(user_id, session):
            return 1
        else:
            return 0

    def get_order_list(self, user_id: str, session: Session) -> Optional[List[str]]:
        order_list = session.query(OrderSQL).filter_by(user_id=user_id).all()
        order_list = [i.order_id for i in order_list]
        order_list = list(set(order_list))
        return order_list
