import logging
import sys

from fastapi import FastAPI, Request

from fast_zero.routers import auth, todos, users
from fast_zero.schemas import Message

# Configurar logging para saída no console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todos.router)


@app.get('/', response_model=Message)
def read_root(request: Request):
    logger.info(f'Requisição GET / - {request._headers}')
    return {'message': 'Olá Mundo!'}
