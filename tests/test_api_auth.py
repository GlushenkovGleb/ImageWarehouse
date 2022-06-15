import pytest

from app.models import Token, UserCreate


def test_sign_up_ok(client_test):
    user_data = UserCreate(login='new_user', password='password').dict()
    response = client_test.post('/auth/sign-up/', json=user_data)

    assert response.status_code == 201
    assert Token.parse_obj(response.json())


def test_sign_up_bad(client_test):
    user_data = UserCreate(login='user', password='password').dict()
    response = client_test.post('/auth/sign-up/', json=user_data)

    assert response.status_code == 409
    assert response.json() == {'detail': 'User with this login already exists'}


def test_sign_in_ok(client_test):
    user_form_data = {'username': 'user', 'password': 'password'}
    response = client_test.post('/auth/sign-in/', data=user_form_data)

    assert response.status_code == 201
    assert Token.parse_obj(response.json())


@pytest.mark.parametrize(
    'user_form_data',
    (
        ({'username': 'NO_USER', 'password': 'password'}),
        ({'username': 'user', 'password': 'NO_PASSWORD'}),
    ),
)
def test_sign_in_bad(client_test, user_form_data):
    response = client_test.post('/auth/sign-in/', data=user_form_data)

    assert response.status_code == 401
    assert response.json() == {'detail': 'Incorrect username or password'}
