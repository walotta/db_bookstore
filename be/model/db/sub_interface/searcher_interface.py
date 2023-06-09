from typing import List, Dict, Any, Optional, Union, Tuple
from ...template.book_info import BookInfoTemp
from ...template.sqlClass.store_book_sql import StoreBookSQL
from ...template.sqlClass.book_info_pic_sql import BookInfoPicSQL
from ...template.sqlClass.book_info_sql import BookInfoSQL
from ...template.sqlClass.book_info_tags_sql import BookInfoTagsSQL
from ..db_client import DBClient
from sqlalchemy import join, func
from sqlalchemy.orm import Session


class SearcherInterface:
    def __init__(self):
        pass

    def get_one_info_by_info_id(
        self, info_id: str, dictName: str, session: Session
    ) -> Optional[Union[str, int, List[str]]]:
        """
        This function will return a single information of match info_id
        """
        result = (
            session.query(getattr(BookInfoSQL, dictName))
            .filter(BookInfoSQL.book_id == info_id)
            .first()
        )
        if result is None:
            return None
        else:
            return result[0]

    def find_book_with_one_dict_n(
        self,
        dict_name: str,
        value: Union[int, str],
        session: Session,
        store_id: Optional[str] = None,
    ) -> int:
        if store_id is None:
            result = (
                session.query(BookInfoSQL)
                .filter(getattr(BookInfoSQL, dict_name) == value)
                .count()
            )
        else:
            stat = join(
                BookInfoSQL, StoreBookSQL, BookInfoSQL.book_id == StoreBookSQL.book_id
            )
            result = (
                session.query(BookInfoSQL)
                .select_from(stat)
                .filter(StoreBookSQL.store_id == store_id)
                .filter(getattr(BookInfoSQL, dict_name) == value)
                .count()
            )
        return result

    def find_book_with_one_dict(
        self,
        dict_name: str,
        value: Union[int, str],
        st: int,
        ed: int,
        return_dict: List[str],
        session: Session,
        store_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        This function could search books with one dict matching.
        Input:
            dict_name:  str
            value:      str/int
            st:         int
            ed:         int
            return_dict List[str]

        Output:
            List[Dict[str, Any]]

        The st and ed normally satisfy ed-st+1=20, and it will be 1-base
        Nomally we would require 'store_id' and 'book_id' and 'title' in return_dict
        The function returns some books with book[dictName]=value
        This function would not search by book_id
        """
        stat = join(
            BookInfoSQL, StoreBookSQL, BookInfoSQL.book_id == StoreBookSQL.book_id
        )
        if store_id is None:
            result = (
                session.query(BookInfoSQL.book_id, StoreBookSQL.store_id)
                .select_from(stat)
                .filter(getattr(BookInfoSQL, dict_name) == value)
                .slice(st - 1, ed)
                .all()
            )
        else:
            result = (
                session.query(BookInfoSQL.book_id, StoreBookSQL.store_id)
                .select_from(stat)
                .filter(StoreBookSQL.store_id == store_id)
                .filter(getattr(BookInfoSQL, dict_name) == value)
                .slice(st - 1, ed)
                .all()
            )
        ans = []
        for r in result:
            tmp = dict()
            for k in return_dict:
                if k == "store_id":
                    v = r[1]
                else:
                    v = self.get_one_info_by_info_id(r[0], k, session)
                tmp[k] = v
            ans.append(tmp)
        return ans

    def find_book_with_content_n(
        self, content_piece: str, session: Session, store_id: Optional[str] = None
    ) -> int:
        stat = join(
            BookInfoSQL, StoreBookSQL, BookInfoSQL.book_id == StoreBookSQL.book_id
        )
        if store_id is None:
            result = (
                session.query(BookInfoSQL)
                .select_from(stat)
                .filter(BookInfoSQL.content.like(f"%{content_piece}%"))
                .count()
            )
        else:
            result = (
                session.query(BookInfoSQL)
                .select_from(stat)
                .filter(StoreBookSQL.store_id == store_id)
                .filter(BookInfoSQL.content.like(f"%{content_piece}%"))
                .count()
            )
        return result

    def find_book_with_content(
        self,
        content_piece: str,
        st: int,
        ed: int,
        return_dict: List[str],
        session: Session,
        store_id: Optional[str] = None,
    ) -> List[Dict[str, str]]:
        """
        This function returns a book_id which have a part of content_piece
        """
        stat = join(
            BookInfoSQL, StoreBookSQL, BookInfoSQL.book_id == StoreBookSQL.book_id
        )
        if store_id is None:
            result = (
                session.query(BookInfoSQL.book_id, StoreBookSQL.store_id)
                .select_from(stat)
                .filter(BookInfoSQL.content.like(f"%{content_piece}%"))
                .slice(st - 1, ed)
                .all()
            )
        else:
            result = (
                session.query(BookInfoSQL.book_id, StoreBookSQL.store_id)
                .select_from(stat)
                .filter(StoreBookSQL.store_id == store_id)
                .filter(BookInfoSQL.content.like(f"%{content_piece}%"))
                .slice(st - 1, ed)
                .all()
            )
        ans = []
        for r in result:
            tmp = dict()
            for k in return_dict:
                if k == "store_id":
                    v = r[1]
                else:
                    v = self.get_one_info_by_info_id(r[0], k, session)
                tmp[k] = v
            ans.append(tmp)
        return ans

    def get_book_tags(
        self, book_id: str, session: Session, store_id: Optional[str] = None
    ) -> List[str]:
        if store_id is None:
            result = session.query(BookInfoTagsSQL.tag).filter_by(book_id=book_id).all()
        else:
            stat = join(
                BookInfoTagsSQL,
                StoreBookSQL,
                BookInfoTagsSQL.book_id == StoreBookSQL.book_id,
            )
            result = (
                session.query(BookInfoTagsSQL.tag)
                .select_from(stat)
                .filter(StoreBookSQL.store_id == store_id)
                .filter(BookInfoTagsSQL.book_id == book_id)
                .all()
            )
        return [i[0] for i in result]

    def find_book_with_tag_n(
        self, tags: List[str], session: Session, store_id: Optional[str] = None
    ) -> int:
        subq = (
            session.query(BookInfoTagsSQL.book_id.label("bid"))
            .filter(BookInfoTagsSQL.tag.in_(tags))
            .group_by(BookInfoTagsSQL.book_id)
            .having(func.count(BookInfoTagsSQL.book_id) == len(tags))
            .subquery()
        )
        stat = join(StoreBookSQL, subq, StoreBookSQL.book_id == subq.c.bid)
        if store_id is None:
            result = (
                session.query(subq.c.bid, StoreBookSQL.store_id)
                .select_from(stat)
                .count()
            )
        else:
            result = (
                session.query(subq.c.bid, StoreBookSQL.store_id)
                .select_from(stat)
                .filter(StoreBookSQL.store_id == store_id)
                .count()
            )
        return result

    def find_book_with_tag(
        self,
        tags: List[str],
        st: int,
        ed: int,
        return_dict: List[str],
        session: Session,
        store_id: Optional[str] = None,
    ) -> List[Dict[str, str]]:
        """
        This function returns a book_id which have a tag
        """
        subq = (
            session.query(BookInfoTagsSQL.book_id.label("bid"))
            .filter(BookInfoTagsSQL.tag.in_(tags))
            .group_by(BookInfoTagsSQL.book_id)
            .having(func.count(BookInfoTagsSQL.book_id) == len(tags))
            .subquery()
        )
        stat = join(StoreBookSQL, subq, StoreBookSQL.book_id == subq.c.bid)
        if store_id is None:
            result = (
                session.query(subq.c.bid, StoreBookSQL.store_id)
                .select_from(stat)
                .slice(st - 1, ed)
                .all()
            )
        else:
            result = (
                session.query(subq.c.bid, StoreBookSQL.store_id)
                .select_from(stat)
                .filter(StoreBookSQL.store_id == store_id)
                .slice(st - 1, ed)
                .all()
            )
        ans = []
        for r in result:
            tmp = dict()
            for k in return_dict:
                if k == "store_id":
                    v = r[1]
                else:
                    v = self.get_one_info_by_info_id(r[0], k, session)
                tmp[k] = v
            ans.append(tmp)
        return ans
