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
