from ..db_client import DBClient
from ...template.store_template import StoreBookTmp, StoreTemp
from ...template.sqlClass.store_book_sql import StoreBookSQL
from ...template.sqlClass.store_sql import StoreSQL
from ...template.sqlClass.book_info_sql import BookInfoSQL
from ...template.sqlClass.book_info_pic_sql import BookInfoPicSQL
from ...template.sqlClass.book_info_tags_sql import BookInfoTagsSQL
from ... import error
from typing import List, Dict, Any, Optional
from ...template.book_info import BookInfoTemp


class StoreInterface:
    def __init__(self, conn: DBClient):
        self.session_maker = conn.DBsession

    def book_id_exist(self, store_id, book_id) -> bool:
        session = self.session_maker()
        match_book = (
            session.query(StoreBookSQL)
            .filter_by(store_id=store_id, book_id=book_id)
            .first()
        )
        session.close()
        return match_book is not None

    def store_id_exist(self, store_id) -> bool:
        session = self.session_maker()
        match_store = session.query(StoreSQL).filter_by(store_id=store_id).first()
        session.close()
        return match_store is not None

    def find_book(self, store_id: str, book_id: str) -> Optional[StoreBookTmp]:
        session = self.session_maker()
        match_book = (
            session.query(StoreBookSQL)
            .filter_by(store_id=store_id, book_id=book_id)
            .first()
        )
        session.close()
        if match_book is None:
            return None
        else:
            return StoreBookTmp(
                match_book.book_id, match_book.book_id, match_book.stock_level
            )

    def get_book_info(self, book_info_id: str) -> Optional[Dict[str, Any]]:
        session = self.session_maker()
        match_book_info = (
            session.query(BookInfoSQL).filter_by(book_id=book_info_id).first()
        )
        session.close()
        if match_book_info is None:
            return None
        else:
            return match_book_info.to_dict()

    def add_stock_level(self, store_id: str, book_id: str, count: int) -> int:
        session = self.session_maker()
        match_book = (
            session.query(StoreBookSQL)
            .filter_by(store_id=store_id, book_id=book_id)
            .first()
        )
        if match_book is None:
            session.close()
            return 0
        else:
            match_book.stock_level += count
            if match_book.stock_level < 0:
                session.close()
                return 0
            session.add(match_book)
            session.commit()
            session.close()
            return 1

    def get_store_seller_id(self, store_id: str) -> Optional[str]:
        session = self.session_maker()
        match_store = session.query(StoreSQL).filter_by(store_id=store_id).first()
        session.close()
        if match_store is None:
            return None
        else:
            return match_store.user_id

    def insert_one_book(
        self, store_id: str, book_id: str, stock_level: int, book_info: str
    ) -> None:
        session = self.session_maker()

        book_info_dict = BookInfoTemp(book_info, store_id).to_dict()
        assert book_id == book_info_dict["book_id"]

        if session.query(BookInfoSQL).filter_by(book_id=book_id).count() == 0:
            book_info_dict = BookInfoTemp(book_info, store_id).to_dict()
            tags = book_info_dict.pop("tags")
            pictures = book_info_dict.pop("pictures")
            for t in tags:
                new_tag = BookInfoTagsSQL(book_id=book_id, tag=t)
                session.add(new_tag)
            for p in pictures:
                new_pic = BookInfoPicSQL(book_id=book_id, pic=p)
                session.add(new_pic)
            new_book_info = BookInfoSQL.from_dict(book_info_dict)
            session.add(new_book_info)
        new_book = StoreBookSQL(
            store_id=store_id, book_id=book_id, stock_level=stock_level
        )
        session.add(new_book)
        session.commit()
        session.close()

    def insert_one_store(self, new_store: StoreTemp) -> None:
        # self.storeCol.insert_one(new_store.to_dict())
        assert len(new_store.book_list) == 0
        session = self.session_maker()
        new_store_sql = StoreSQL.from_dict(new_store.to_dict())
        session.add(new_store_sql)
        session.commit()
        session.close()
