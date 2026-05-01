from http import HTTPStatus

import factory
import factory.fuzzy
import pytest

from fast_zero.models import Todo, TodoState


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = factory.Faker('text', max_nb_chars=20, locale='pt_BR')
    description = factory.Faker('text', max_nb_chars=100, locale='pt_BR')
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = 1


@pytest.mark.asyncio
async def test_list_todos_should_return_5_todos(session, client, user, token):
    expected_todos = 5

    session.add_all(TodoFactory.create_batch(expected_todos, user_id=user.id))
    await session.commit()

    response = client.get(
        '/todos/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_pagination_should_return_2_todos(
    session, client, user, token
):

    expected_todos = 2

    session.add_all(TodoFactory.create_batch(5, user_id=user.id))
    await session.commit()

    response = client.get(
        '/todos/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_filter_title_should_return_5_todos(
    session, client, user, token
):

    expected_todos = 5

    session.add_all(
        TodoFactory.create_batch(
            expected_todos, user_id=user.id, title='Title todo 1'
        )
    )
    await session.commit()

    response = client.get(
        '/todos/?title=Title todo 1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_filter_description_should_return_5_todos(
    session, client, user, token
):

    expected_todos = 5

    session.add_all(
        TodoFactory.create_batch(
            expected_todos, user_id=user.id, description='Description todo 1'
        )
    )
    await session.commit()

    response = client.get(
        '/todos/?description=Description todo 1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_filter_state_should_return_5_todos(
    session, client, user, token
):

    expected_todos = 5

    session.add_all(
        TodoFactory.create_batch(
            expected_todos, user_id=user.id, state=TodoState.todo
        )
    )
    await session.commit()

    response = client.get(
        '/todos/?state=todo',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


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

    res_json = response.json()
    assert res_json['title'] == 'Test Todo'
    assert res_json['description'] == 'This is a test todo'
    assert res_json['state'] == 'todo'
    assert 'created_at' in res_json
    assert 'updated_at' in res_json


def test_list_empty_todos(client, token):
    reponse = client.get(
        '/todos/', headers={'Authorization': f'Bearer {token}'}
    )
    assert reponse.status_code == HTTPStatus.OK
    assert reponse.json() == {'todos': []}


@pytest.mark.asyncio
async def test_delete_todo(session, client, user, token):
    # arrange
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    await session.commit()

    # act
    response = client.delete(
        f'/todos/{todo.id}', headers={'Authorization': f'Bearer {token}'}
    )

    # assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Task has been deleted successfully'}


def test_delete_todo_not_found(client, token):
    response = client.delete(
        '/todos/999', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}


@pytest.mark.asyncio
async def test_delete_other_user_todo(session, client, other_user, token):
    todo_other_user = TodoFactory(user_id=other_user.id)
    session.add(todo_other_user)
    await session.commit()

    response = client.delete(
        f'/todos/{todo_other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}


@pytest.mark.asyncio
async def test_update_todo_not_found(client, token):
    response = client.patch(
        '/todos/10',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}


@pytest.mark.asyncio
async def test_update_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    await session.commit()

    response = client.patch(
        f'/todos/{todo.id}',
        json={'title': 'teste!'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'teste!'
