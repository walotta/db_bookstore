from sqlalchemy import create_engine
from be.model.template.sqlClass.base import Base


def delete_database():
    engine = create_engine(
        "postgresql://postgres:postgres@localhost:5432/postgres",
        pool_size=8,
        pool_recycle=60 * 30,
    )
    Base.metadata.drop_all(engine)


if __name__ == "__main__":
    delete_database()
