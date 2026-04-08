import logging
import sys
from http import HTTPStatus

from fastapi import FastAPI, HTTPException, Request

from fast_zero.schemas import Message, UserDb, UserList, UserPublic, UserSchema

# Configurar logging para saída no console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

app = FastAPI()

database = []  # Simulação de banco de dados em memória


@app.get('/', response_model=Message)
def read_root(request: Request):
    logger.info(f'Requisição GET / - {request._headers}')
    return {'message': 'Olá Mundo!'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    # breakpoint()  # Ponto de interrupção para depuração l entra q sai
    user_with_id = UserDb(**user.model_dump(), id=len(database) + 1)
    database.append(user_with_id)
    logger.info(f'Usuario criado: {user_with_id.id} - {user_with_id.username}')
    return user_with_id


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users():
    return {'users': database}


@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='USER NOT FOUND'
        )
    user_with_id = UserDb(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id
    return user_with_id
