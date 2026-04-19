from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User

# SECRET_KEY = Settings().SECRET_KEY
# ALGORITHM = Settings().ALGORITHM
# ACCESS_TOKEN_EXPIRE_MINUTES = Settings().ACCESS_TOKEN_EXPIRE_MINUTES
# TIME_ZONE = Settings().TIME_ZONE

ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = 'your_secret_key'
ALGORITHM = 'HS256'
TIME_ZONE = 'America/Porto_Velho'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')

pwd_context = PasswordHash.recommended()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
):

    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        subject_email = payload.get('sub')
        if not subject_email:
            raise credentials_exception

    except DecodeError:
        raise credentials_exception

    user = session.scalar(select(User).where(User.email == subject_email))

    if not user:
        raise credentials_exception

    return user


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):

    to_encode = data.copy()

    # Adiciona um tempo de expiração ao token
    expire = datetime.now(tz=ZoneInfo(TIME_ZONE)) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp': expire})

    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
