import logging
import sys
from http import HTTPStatus

from fastapi import FastAPI, Request

from fast_zero.schemas import Message, UserPublic, UserSchema

# Configurar logging para saída no console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get('/', response_model=Message)
def read_root(request: Request):
    logger.info(f'Requisição GET / - {request._headers}')
    return {'message': 'Olá Mundo!'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    # breakpoint()  # Ponto de interrupção para depuração l entra q sai
    logger.info(f'Usuario criado: {user.username} - {user.email} - {user.password}')
    return user
