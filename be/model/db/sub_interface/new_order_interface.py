from ..db_client import DBClient
from ...template.new_order_template import NewOrderTemp, NewOrderBookItemTemp
from ...template.sqlClass.order_sql import OrderSQL
from typing import Optional, List, Dict, Any
from ...template.new_order_template import STATUS


class NewOrderInterface:
    def __init__(self, conn: DBClient):
        self.session_maker = conn.DBsession

    def insert_new_order(self, new_order: NewOrderTemp):
        session = self.session_maker()
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
        session.commit()
        session.close()

    def find_new_order(self, order_id: str) -> Optional[NewOrderTemp]:
        session = self.session_maker()
        orders = session.query(OrderSQL).filter_by(order_id=order_id).all()
        session.close()
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

    def delete_order(self, order_id: str) -> int:
        session = self.session_maker()
        result = session.query(OrderSQL).filter_by(order_id=order_id).delete()
        session.commit()
        session.close()
        return result

    def order_id_exist(self, order_id: str) -> bool:
        session = self.session_maker()
        match_order = session.query(OrderSQL).filter_by(order_id=order_id).first()
        session.close()
        return match_order is not None

    def update_new_order_status(self, order_id: str, status: STATUS) -> int:
        session = self.session_maker()
        result = (
            session.query(OrderSQL)
            .filter_by(order_id=order_id)
            .update({"status": status.value})
        )
        session.commit()
        session.close()
        return result

    def find_order_status(self, order_id: str) -> Optional[STATUS]:
        session = self.session_maker()
        result = session.query(OrderSQL).filter_by(order_id=order_id).first()
        session.close()
        if result is None:
            return None
        else:
            return STATUS(result.status)

    def auto_cancel_expired_order(
        self, current_time: int, expire_time: int
    ) -> List[str]:
        # for all order that satisfy order.create_time + expire_time >= current_time
        # and status == INIT(0), change its status to CANCELLED(4)
        # returns: a list of order_id, represent all cancelled order

        session = self.session_maker()
        result = session.query(OrderSQL).filter_by(status=0).all()
        session.close()
        order_id_list = []
        for o in result:
            if o.create_time + expire_time >= current_time:
                order_id_list.append(o.order_id)
                self.update_new_order_status(o.order_id, STATUS.CANCELED)
        return order_id_list
