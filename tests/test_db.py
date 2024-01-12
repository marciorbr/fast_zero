from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.models import Todo, User


def test_create_user(session):
    user = User(username='test', email='test@test.com', password='secret')
    session.add(user)
    session.commit()

    result = session.scalar(select(User).where(User.email == 'test@test.com'))

    # assert
    assert result == user


def test_create_todo(session: Session, user: User):
    todo = Todo(
        title='Test Todo',
        description='Test Desc',
        state='draft',
        user_id=user.id,
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    user = session.scalar(select(User).where(User.id == user.id))

    assert todo in user.todos
