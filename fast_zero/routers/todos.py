from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_zero.database import get_session
from fast_zero.models import Todo, User
from fast_zero.schemas import (
    FilterTodo,
    Message,
    TodoList,
    TodoPublic,
    TodoSchema,
    TodoUpdate,
)
from fast_zero.security import get_current_user

router = APIRouter(prefix='/todos', tags=['todos'])

T_Session = Annotated[AsyncSession, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=TodoPublic)
async def create_todo(
    todo: TodoSchema,
    user: T_CurrentUser,
    session: T_Session,
):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )
    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)

    return db_todo


@router.get('/', status_code=HTTPStatus.OK, response_model=TodoList)
async def list_todos(
    user: T_CurrentUser,
    session: T_Session,
    todo_filter: Annotated[FilterTodo, Query()],
):
    query = select(Todo).where(Todo.user_id == user.id)

    if todo_filter.title:
        query = query.filter(Todo.title.contains(todo_filter.title))
    if todo_filter.description:
        query = query.filter(
            Todo.description.contains(todo_filter.description)
        )
    if todo_filter.state:
        query = query.filter(Todo.state == todo_filter.state)

    todos = await session.scalars(
        query.offset(todo_filter.offset).limit(todo_filter.limit)
    )

    return {'todos': todos.all()}


@router.delete('/{todo_id}', response_model=Message)
async def delete_todo(
    todo_id: int,
    user: T_CurrentUser,
    session: T_Session,
):
    todo = await session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found'
        )

    await session.delete(todo)
    await session.commit()

    return {'message': 'Task has been deleted successfully'}


@router.patch('/{todo_id}', response_model=TodoPublic)
async def update_todo(
    todo_id: int,
    user: T_CurrentUser,
    session: T_Session,
    todo: TodoUpdate,
):
    db_todo = await session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not db_todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found'
        )

    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)

    return db_todo
