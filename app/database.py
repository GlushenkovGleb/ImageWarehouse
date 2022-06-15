import os
from pathlib import Path

import sqlalchemy.orm as so
from minio import Minio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .settings import settings
from .tables import Base  # type: ignore

engine = create_engine(
    settings.database_url,
    connect_args={'check_same_thread': False},
)

Session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
)


def get_session() -> so.Session:  # pragma: no cover
    new_session = Session()
    try:
        yield new_session
        new_session.commit()
    except Exception:
        new_session.rollback()
        raise
    finally:
        new_session.close()


def get_minio() -> Minio:  # pragma: no cover
    client = Minio(
        endpoint=settings.minio_url,
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=settings.minio_secure,
    )
    yield client


def init_db() -> None:  # pragma: no cover
    data_path = Path(settings.data_path)
    if not data_path.exists():
        try:
            os.mkdir('./isinstance')
        except OSError:
            pass
        Base.metadata.create_all(engine)
