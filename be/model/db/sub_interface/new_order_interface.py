from ..db_client import DBClient
from ...template.new_order_template import NewOrderTemp, NewOrderBookItemTemp
from ...template.sqlClass.order_sql import OrderSQL
from typing import Optional, List, Dict, Any
from ...template.new_order_template import STATUS
from sqlalchemy.orm import Session


class NewOrderInterface:
    def __init__(self):
        pass

    def insert_new_order(self, new_order: NewOrderTemp, session: Session):
        for book in new_order.book_list:
            session.add(
                OrderSQL(
                    order_id=new_order.order_id,
                    user_id=new_order.user_id,
                    store_id=new_order.store_id,
                    book_id=book.book_id,
                    count=book.count,
                    price=book.price,
                    create_time=new_order.create_time,
                    status=new_order.status.value,
                )
            )

    def find_new_order(self, order_id: str, session: Session) -> Optional[NewOrderTemp]:
        orders = session.query(OrderSQL).filter_by(order_id=order_id).all()
        if len(orders) == 0:
            return None
        else:
            book_list = []
            for o in orders:
                book_list.append(NewOrderBookItemTemp(o.book_id, o.count, o.price))
            o = orders[0]
            return NewOrderTemp(
                o.order_id,
                o.user_id,
                o.store_id,
                book_list,
                o.create_time,
                STATUS(o.status),
            )

    def delete_order(self, order_id: str, session: Session) -> int:
        result = session.query(OrderSQL).filter_by(order_id=order_id).delete()
        return result

    def order_id_exist(self, order_id: str, session: Session) -> bool:
        match_order = session.query(OrderSQL).filter_by(order_id=order_id).first()
        return match_order is not None

    def update_new_order_status(
        self, order_id: str, status: STATUS, session: Session
    ) -> int:
        result = (
            session.query(OrderSQL)
            .filter_by(order_id=order_id)
            .update({"status": status.value})
        )
        return result

    def find_order_status(self, order_id: str, session: Session) -> Optional[STATUS]:
        result = session.query(OrderSQL).filter_by(order_id=order_id).first()
        if result is None:
            return None
        else:
            return STATUS(result.status)

    def auto_cancel_expired_order(
        self, current_time: int, expire_time: int, session: Session
    ) -> List[str]:
        # for all order that satisfy order.create_time + expire_time >= current_time
        # and status == INIT(0), change its status to CANCELLED(4)
        # returns: a list of order_id, represent all cancelled order

        result = session.query(OrderSQL).filter_by(status=0).all()
        order_id_list = []
        for o in result:
            if o.create_time + expire_time >= current_time:
                order_id_list.append(o.order_id)
                self.update_new_order_status(o.order_id, STATUS.CANCELED, session)
        return order_id_list
