from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from database import get_db
from crud import users as crud_user
from schemas.users import UserCreate, UserResponse
from typing import  List
router = APIRouter()


@router.get("/", response_model=List[UserResponse])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        return crud_user.get_all_users(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
@router.post("/")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        created =  crud_user.register_user(db, user)
        if created:
            return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "User registered successfully!"})
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "User already exist!"})

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))