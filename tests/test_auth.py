from http import HTTPStatus


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
