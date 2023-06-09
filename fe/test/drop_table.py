from sqlalchemy import create_engine, text


def drop_all():
    engine = create_engine(
        "postgresql://postgres:postgres@127.0.0.1:5432/postgres",
        pool_size=8,
        pool_recycle=60 * 30,
    )
    conn = engine.connect()
    table_names = [
        "bookinfo",
        "bookinfopic",
        "bookinfosql",
        "bookinfotags",
        '"order"',
        "storebook",
        "store",
        '"user"',  # quote here since user is a reserved word in postgresql
    ]
    sequence_names = [
        "bookinfopic__id_seq",
        "bookinfotags__id_seq",
        "order__id_seq",
        "storebook__id_seq",
    ]
    for tn in table_names:
        conn.execute(text(f"DROP TABLE IF EXISTS {tn} CASCADE"))
    for sn in sequence_names:
        conn.execute(text(f"DROP SEQUENCE IF EXISTS {sn} CASCADE"))
    conn.close()


if __name__ == "__main__":
    drop_all()
