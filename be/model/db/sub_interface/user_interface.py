from ..db_client import DBClient
from ...template.user_template import UserTemp
from ...template.sqlClass.user_sql import UserSQL
from ...template.sqlClass.order_sql import OrderSQL
from typing import Optional, List


class UserInterface:
    def __init__(self, conn: DBClient):
        self.session_maker = conn.DBsession

    def user_id_exist(self, user_id: str) -> bool:
        session = self.session_maker()
        match_user = session.query(UserSQL).filter_by(user_id=user_id).first()
        session.close()
        return match_user is not None

    def add_balance(self, user_id: str, count: int) -> int:
        session = self.session_maker()
        match_user = session.query(UserSQL).filter_by(user_id=user_id).first()
        if match_user is None:
            session.close()
            return 0
        match_user.balance += count
        if match_user.balance < 0:
            session.close()
            return 0
        session.add(match_user)
        session.commit()
        session.close()
        return 1

    def get_password(self, user_id: str) -> Optional[str]:
        session = self.session_maker()
        match_user = session.query(UserSQL).filter_by(user_id=user_id).first()
        session.close()
        if match_user is None:
            return None
        else:
            return match_user.password

    def get_balance(self, user_id: str) -> Optional[int]:
        session = self.session_maker()
        match_user = session.query(UserSQL).filter_by(user_id=user_id).first()
        session.close()
        if match_user is None:
            return None
        else:
            return match_user.balance

    def get_token(self, user_id: str) -> Optional[str]:
        session = self.session_maker()
        match_user = session.query(UserSQL).filter_by(user_id=user_id).first()
        session.close()
        if match_user is None:
            return None
        else:
            return match_user.token

    def insert_one_user(self, user: UserTemp) -> None:
        assert len(user.order_id_list) == 0
        session = self.session_maker()
        user_sql = UserSQL.from_dict(user.to_dict())
        session.add(user_sql)
        session.commit()
        session.close()

    def update_token_terminal(self, user_id: str, token: str, terminal: str) -> int:
        session = self.session_maker()
        match_user = session.query(UserSQL).filter_by(user_id=user_id).first()
        if match_user is None:
            session.close()
            return 0
        match_user.token = token
        match_user.terminal = terminal
        session.add(match_user)
        session.commit()
        session.close()
        return 1

    def delete_user(self, user_id: str) -> int:
        session = self.session_maker()
        match_user = session.query(UserSQL).filter_by(user_id=user_id).first()
        if match_user is None:
            session.close()
            return 0
        session.delete(match_user)
        session.commit()
        session.close()
        return 1

    def update_password(
        self, user_id: str, password: str, token: str, terminal: str
    ) -> int:
        session = self.session_maker()
        match_user = session.query(UserSQL).filter_by(user_id=user_id).first()
        if match_user is None:
            session.close()
            return 0
        match_user.password = password
        match_user.token = token
        match_user.terminal = terminal
        session.add(match_user)
        session.commit()
        session.close()
        return 1

    def add_order(self, user_id: str, order_id: str) -> int:
        if self.user_id_exist(user_id):
            return 1
        else:
            return 0

    def get_order_list(self, user_id: str) -> Optional[List[str]]:
        session = self.session_maker()
        order_list = session.query(OrderSQL).filter_by(user_id=user_id).all()
        session.close()
        order_list = [i.order_id for i in order_list]
        order_list = list(set(order_list))
        return order_list
