from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jwt import encode
from pwdlib import PasswordHash

# SECRET_KEY = Settings().SECRET_KEY
# ALGORITHM = Settings().ALGORITHM
# ACCESS_TOKEN_EXPIRE_MINUTES = Settings().ACCESS_TOKEN_EXPIRE_MINUTES
# TIME_ZONE = Settings().TIME_ZONE

ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = 'your_secret_key'
ALGORITHM = 'HS256'
TIME_ZONE = 'America/Porto_Velho'


pwd_context = PasswordHash.recommended()


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
