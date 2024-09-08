from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from crud import auth as crud_auth
from crud import users as crud_user
from crud.auth import generate_token
from database import get_db
from schemas.auth import Login
from schemas.token import RefreshToken, Token
from schemas.users import UserCreate
from utils.jwt import decode_token, token_expired

router = APIRouter()


@router.post("/refresh-token")
def new__token(token: RefreshToken):
    refresh_token = token.refresh_token
    payload = decode_token(refresh_token)
    email = payload.get("email", None)
    type = payload.get("type", None)

    if type is None or email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    if type != "Refresh Token":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Token"
        )

    is_expired = token_expired(refresh_token)
    if is_expired:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )

    return generate_token(email)


@router.post("/sign-up")
def register_user(user: UserCreate, db: Session = Depends(get_db)) -> JSONResponse:
    try:
        created = crud_user.register_user(db, user)
        if created:
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={"message": "User registered successfully!"},
            )
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": "User already exist!"}
        )

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/sign-in")
def login_user(user_login: Login, db: Session = Depends(get_db)) -> Token:
    logged_in = crud_auth.login_user(db, user_login)
    if logged_in:
        return generate_token(user_login.email)
