from .db_client import DBClient, get_db_conn


class DBConn:
    def __init__(self):
        self.conn: DBClient = get_db_conn()

    def user_id_exist(self, user_id) -> bool:
        cursor = self.conn.userCol.find_one({"user_id": user_id})
        return cursor is not None

    def book_id_exist(self, store_id, book_id) -> bool:
        cursor = self.conn.storeCol.find_one(
            {"store_id": store_id, "book_list.book_id": book_id}
        )
        return cursor is not None

    def store_id_exist(self, store_id) -> bool:
        cursor = self.conn.storeCol.find_one({"store_id": store_id})
        return cursor is not None
