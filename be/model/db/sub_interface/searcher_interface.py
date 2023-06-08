from typing import List, Dict, Any, Optional, Union, Tuple
from ...template.book_info import BookInfoTemp
from ...template.sqlClass.store_book_sql import StoreBookSQL
from ...template.sqlClass.book_info_pic_sql import BookInfoPicSQL
from ...template.sqlClass.book_info_sql import BookInfoSQL
from ...template.sqlClass.book_info_tags_sql import BookInfoTagsSQL
from ..db_client import DBClient
from sqlalchemy import join
import re


class SearcherInterface:
    def __init__(self, conn: DBClient):
        self.session_maker = conn.DBsession
        self.engine = conn.engine

    def get_one_info_by_info_id(
        self, info_id: str, dictName: str
    ) -> Optional[Union[str, int, List[str]]]:
        """
        This function will return a single information of match info_id
        """
        with self.engine.connect() as conn:
            result = conn.execute(
                f"SELECT {dictName} FROM bookinfo WHERE book_id = '{info_id}'"
            ).fetchone()
            if result is None:
                return None
            else:
                return result[0]

    def find_book_with_one_dict_n(
        self, dict_name: str, value: Union[int, str], store_id: Optional[str] = None
    ) -> int:
        with self.engine.connect() as conn:
            if store_id is None:
                result = conn.execute(
                    f"SELECT COUNT(*) FROM bookinfo WHERE {dict_name} = '{value}'"
                ).fetchone()
            else:
                result = conn.execute(
                    f"""SELECT COUNT(*)
                    FROM bookinfo bi
                    JOIN storebook si ON si.book_id = bi.book_id
                    WHERE bi.{dict_name} = '{value}' AND si.store_id = '{store_id}'"""
                ).fetchone()
        if result is None:
            return 0
        else:
            return result[0]

    def find_book_with_one_dict(
        self,
        dict_name: str,
        value: Union[int, str],
        st: int,
        ed: int,
        return_dict: List[str],
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
        with self.engine.connect() as conn:
            if store_id is None:
                result = conn.execute(
                    f"""SELECT bi.book_id, si.store_id 
                    FROM bookinfo bi
                    JOIN storebook si ON si.book_id = bi.book_id
                    WHERE bi.{dict_name} = '{value}' LIMIT {ed-st+1} OFFSET {st-1}"""
                ).fetchall()
            else:
                result = conn.execute(
                    f"""SELECT bi.book_id, si.store_id 
                    FROM bookinfo bi
                    JOIN storebook si ON si.book_id = bi.book_id
                    WHERE si.store_id = '{store_id}' AND bi.{dict_name} = '{value}' LIMIT {ed-st+1} OFFSET {st-1}"""
                ).fetchall()
        ans = []
        for r in result:
            tmp = dict()
            for k in return_dict:
                if k == "store_id":
                    v = r[1]
                else:
                    v = self.get_one_info_by_info_id(r[0], k)
                tmp[k] = v
            ans.append(tmp)
        return ans

    def find_book_with_content_n(
        self, content_piece: str, store_id: Optional[str] = None
    ) -> int:
        session = self.session_maker()
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
        session.close()
        return result

    def find_book_with_content(
        self,
        content_piece: str,
        st: int,
        ed: int,
        return_dict: List[str],
        store_id: Optional[str] = None,
    ) -> List[Dict[str, str]]:
        """
        This function returns a book_id which have a part of content_piece
        """
        session = self.session_maker()
        stat = join(
            BookInfoSQL, StoreBookSQL, BookInfoSQL.book_id == StoreBookSQL.book_id
        )
        if store_id is None:
            result = (
                session.query(BookInfoSQL.book_id, StoreBookSQL.store_id)
                .select_from(stat)
                .filter(BookInfoSQL.content.like(f"%{content_piece}%"))
                .limit(ed - st + 1)
                .offset(st - 1)
                .all()
            )
        else:
            result = (
                session.query(BookInfoSQL.book_id, StoreBookSQL.store_id)
                .select_from(stat)
                .filter(StoreBookSQL.store_id == store_id)
                .filter(BookInfoSQL.content.like(f"%{content_piece}%"))
                .limit(ed - st + 1)
                .offset(st - 1)
                .all()
            )
        session.close()
        ans = []
        for r in result:
            tmp = dict()
            for k in return_dict:
                if k == "store_id":
                    v = r[1]
                else:
                    v = self.get_one_info_by_info_id(r[0], k)
                tmp[k] = v
            ans.append(tmp)
        return ans

    def get_book_tags(self, book_id: str, store_id: Optional[str] = None) -> List[str]:
        session = self.session_maker()
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
        session.close()
        return [i[0] for i in result]

    def find_book_with_tag_n(
        self, tags: List[str], store_id: Optional[str] = None
    ) -> int:
        with self.engine.connect() as conn:
            tag_list = f"({str(tags)[1:-1]})"
            if store_id is None:
                result = conn.execute(
                    f"""SELECT COUNT(t.book_id)
                        FROM storebook si
                        JOIN (
                            SELECT bt.book_id
                            FROM bookinfotags bt
                            WHERE bt.tag IN {tag_list}
                            GROUP BY bt.book_id
                            HAVING COUNT(bt.book_id) = {len(tags)}
                        ) t ON t.book_id = si.book_id"""
                ).fetchone()
            else:
                result = conn.execute(
                    f"""SELECT COUNT(t.book_id)
                        FROM storebook si
                        JOIN (
                            SELECT bt.book_id
                            FROM bookinfotags bt
                            WHERE bt.tag IN {tag_list}
                            GROUP BY bt.book_id
                            HAVING COUNT(bt.book_id) = {len(tags)}
                        ) t ON t.book_id = si.book_id
                        WHERE si.store_id = {store_id}"""
                ).fetchone()
            if result is None:
                return 0
            else:
                return result[0]

    def find_book_with_tag(
        self,
        tags: List[str],
        st: int,
        ed: int,
        return_dict: List[str],
        store_id: Optional[str] = None,
    ) -> List[Dict[str, str]]:
        """
        This function returns a book_id which have a tag
        """
        with self.engine.connect() as conn:
            tag_list = f"({str(tags)[1:-1]})"
            if store_id is None:
                result = conn.execute(
                    f"""SELECT t.book_id, si.store_id
                    FROM storebook si
                    JOIN (
                        SELECT bt.book_id
                        FROM bookinfotags bt
                        WHERE bt.tag IN {tag_list}
                        GROUP BY bt.book_id
                        HAVING COUNT(bt.book_id) = {len(tags)}
                    ) t ON t.book_id = si.book_id
                    LIMIT {ed-st+1} OFFSET {st-1}"""
                ).fetchall()
            else:
                result = conn.execute(
                    f"""SELECT t.book_id, si.store_id
                        FROM storebook si
                        JOIN (
                            SELECT bt.book_id
                            FROM bookinfotags bt
                            WHERE bt.tag IN {tag_list}
                            GROUP BY bt.book_id
                            HAVING COUNT(bt.book_id) = {len(tags)}
                        ) t ON t.book_id = si.book_id
                        WHERE si.store_id = {store_id}
                        LIMIT {ed-st+1} OFFSET {st-1}"""
                ).fetchall()
            ans = []
            for r in result:
                tmp = dict()
                for k in return_dict:
                    if k == "store_id":
                        v = r[1]
                    else:
                        v = self.get_one_info_by_info_id(r[0], k)
                    tmp[k] = v
                ans.append(tmp)
            return ans
