from datetime import datetime, timedelta
from typing import Tuple

from jose import jwt

from env_config import config


def get_timestamp():
    current_timestamp = datetime.now().timestamp()

    current_datetime = datetime.fromtimestamp(current_timestamp)

    expiration_datetime = current_datetime + timedelta(minutes=60)

    expiration_timestamp = expiration_datetime.timestamp()
    return int(expiration_timestamp)


def encode_token(payload: dict) -> Tuple[str, str]:
    expiration = get_timestamp()

    payload["exp"] = expiration

    token = jwt.encode(payload, key=config.SECRET_KEY, algorithm=config.JWT_ALGORITHM)
    return token, expiration


def decode_token(token: str) -> dict:
    return jwt.decode(token, key=config.SECRET_KEY, algorithms=config.JWT_ALGORITHM)
