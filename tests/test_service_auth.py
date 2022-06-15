from datetime import datetime, timedelta

import pytest
from fastapi import HTTPException
from jose import jwt

from app.models import User
from app.service.auth import AuthService
from app.settings import settings


@pytest.fixture(scope='module')
def token_ok() -> str:
    now = datetime.utcnow()
    user_data = User(
        id=1, password_hash=AuthService.get_hashed_password('password'), login='user'
    )
    payload = {
        'iat': now,
        'nbf': now,
        'exp': now + timedelta(minutes=30),
        'sub': '1',
        'user': user_data.dict(),
    }
    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


@pytest.fixture(scope='module')
def token_expire() -> str:
    now = datetime.utcnow()
    user_data = User(
        id=1, password_hash=AuthService.get_hashed_password('password'), login='user'
    )
    payload = {
        'iat': now,
        'nbf': now,
        'exp': now - timedelta(minutes=30),
        'sub': '1',
        'user': user_data.dict(),
    }
    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


@pytest.fixture(scope='module')
def token_no_user() -> str:
    now = datetime.utcnow()
    user_data = 'INVALID USER DATA'
    payload = {
        'iat': now,
        'nbf': now,
        'exp': now + timedelta(minutes=30),
        'sub': '1',
        'user': user_data,
    }
    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def test_check_token_ok(token_ok):
    assert AuthService.check_token(token_ok) is None


def test_check_token_expire(token_expire):
    with pytest.raises(HTTPException) as exc_info:
        AuthService.check_token(token_expire)
    assert 'Could not validate credentials' in str(exc_info)


def test_check_token_no_user(token_no_user):
    with pytest.raises(HTTPException) as exc_info:
        AuthService.check_token(token_no_user)
    assert 'Could not validate credentials' in str(exc_info)
