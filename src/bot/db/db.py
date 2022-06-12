import os
from contextlib import contextmanager
from typing import Iterable

import psycopg2
from psycopg2.extensions import cursor
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import functions

engine = create_engine(
    (
        f"postgresql+psycopg2://{os.environ['POSTGRES_USER']}"
        f":{os.environ['POSTGRES_PASSWORD']}"
        f"@{os.environ['POSTGRES_HOST']}:5432/"
        f"{os.environ['POSTGRES_DB']}"
    ),
    isolation_level="AUTOCOMMIT",
    executemany_mode="values",
    executemany_values_page_size=50000,
)

session = scoped_session(sessionmaker(bind=engine))

@contextmanager
def new_session(**kwargs):
    _session = session(**kwargs)
    try:
        yield _session
    except Exception:
        _session.rollback()
        raise
    else:
        _session.commit()
