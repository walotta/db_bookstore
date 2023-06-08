from sqlalchemy.engine import Engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Any, Optional
from sqlalchemy import create_engine
from ..template.sqlClass.base import Base


class DBClient:
    def __init__(self):
        self.engine: Engine = create_engine(
            "postgresql://postgres:postgres@localhost:5432/postgres",
            pool_size=8,
            pool_recycle=60 * 30,
        )
        self.DBsession = sessionmaker(bind=self.engine)

    def database_init(self) -> None:
        Base.metadata.create_all(self.engine)

    def database_reset(self) -> None:
        self.DBsession.close_all()


database_instance: Optional[DBClient] = None


def db_init() -> None:
    global database_instance
    database_instance = DBClient()
    database_instance.database_init()


def get_db_conn() -> DBClient:
    global database_instance
    assert database_instance is not None, "Database not initialized"
    return database_instance
