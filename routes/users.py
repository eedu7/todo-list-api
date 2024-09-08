from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from crud import auth as crud_auth
from crud import users as crud_user
from crud.auth import generate_token
from database import get_db
from schemas.auth import Login
from schemas.token import Token
from schemas.users import UserCreate, UserResponse

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
def get_users(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> List[UserResponse]:
    try:
        return crud_user.get_all_users(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


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
