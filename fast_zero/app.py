import logging
import sys

from fastapi import FastAPI, Request

# Configurar logging para saída no console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get('/')
def read_root(request: Request):
    logger.info(f'Requisição GET / - {request._headers}')
    return {'message': 'Olá Mundo!'}
