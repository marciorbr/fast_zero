from http import HTTPStatus

from freezegun import freeze_time

from fast_zero.settings import Settings

settings = Settings()

ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def test_get_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clear_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert token['token_type'] == 'bearer'


def test_get_token_user_not_found(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': 'nonexistent@example.com',
            'password': 'wrongpassword',
        },
    )

    token = response.json()

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert token['detail'] == 'Incorrect email or password'


def test_get_token_invalid_credentials(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': 'wrongpassword'},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert token['detail'] == 'Incorrect email or password'


def test_token_expired_after_time(client, user):

    with freeze_time('2023-07-14 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clear_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time(f'2023-07-14 12:{ACCESS_TOKEN_EXPIRE_MINUTES + 1}:00'):
        response = client.put(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'wrongwrong',
                'email': 'wrong@wrong.com',
                'password': 'wrong',
            },
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}
