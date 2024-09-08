from datetime import datetime, timedelta
from typing import Tuple

from fastapi import HTTPException, status
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


def token_expired(token: str) -> bool:
    payload = decode_token(token)
    exp = payload.get("exp", None)
    if exp is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )
    current_time = get_timestamp()

    if exp < current_time:
        return True
    return False
