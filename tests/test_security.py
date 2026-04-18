from http import HTTPStatus

from jwt import decode

from fast_zero.security import ALGORITHM, SECRET_KEY, create_access_token


def test_create_access_token():
    data = {'sub': 'testuser'}
    token = create_access_token(data)
    assert token is not None


def test_decode_access_token():
    data = {'sub': 'testuser'}
    token = create_access_token(data)
    decoded_data = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_data['sub'] == data['sub']
    assert 'exp' in decoded_data


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1',
        headers={'Authorization': 'Bearer invalid_token'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_user_not_found(client):
    # Criar um token com um email que não existe no banco
    token = create_access_token(data={'sub': 'nonexistent_user'})
    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_email_not_found(client):
    # Criar um token com um email que não existe no banco
    token = create_access_token(data={})
    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
