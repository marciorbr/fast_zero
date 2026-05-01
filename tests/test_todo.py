from http import HTTPStatus


def test_create_todo(client, token):
    response = client.post(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test Todo',
            'description': 'This is a test todo',
            'state': 'todo',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'title': 'Test Todo',
        'description': 'This is a test todo',
        'state': 'todo',
    }
