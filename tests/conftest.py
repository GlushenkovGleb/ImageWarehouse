from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.app import app
from app.database import Base, get_session
from app.service.auth import AuthService
from app.tables import Inbox, User

DB_URL_TEST = 'sqlite:///./tests/data/test.sqlite3'

engine = create_engine(DB_URL_TEST, connect_args={'check_same_thread': False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_test_session() -> Generator[Session, None, None]:
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def check_no_auth() -> None:
    pass


app.dependency_overrides[get_session] = get_test_session
app.dependency_overrides[AuthService.check_token] = check_no_auth


def init_db():
    session = TestingSessionLocal()
    session.add(
        User(login='user', password_hash=AuthService.get_hashed_password('password'))
    )
    session.add(Inbox(name='name', frame_id=1))
    session.commit()


@pytest.fixture
def client_test():
    Base.metadata.create_all(engine)
    init_db()
    client = TestClient(app)
    yield client
    Base.metadata.drop_all(engine)


@pytest.fixture
def session() -> Session:
    return TestingSessionLocal()
