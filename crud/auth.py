from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from crud import BasicCrud
from models import User
from schemas.auth import Login
from schemas.token import Token
from utils import jwt
from utils.password import verify_password


def login_user(db: Session, user_login: Login) -> bool:
    try:
        base_crud = BasicCrud(model=User, db_session=db)
        user = base_crud.get_by("email", user_login.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with {user_login.email} not found.",
            )

        if not verify_password(user_login.password, user.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid")
        return True
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


def generate_token(email: str) -> Token:
    payload = {"email": email}
    access_token, exp = jwt.encode_token(payload)
    refresh_token, exp = jwt.encode_token({"type": "Refresh Token", "email": email})
    return Token(access_token=access_token, refresh_token=refresh_token, exp=exp)
