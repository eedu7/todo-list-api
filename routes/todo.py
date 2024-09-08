from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from crud import todo as todo_crud
from database import get_db
from models import User
from schemas.todos import CreateTodo, TodoResponse, UpdateTodo
from utils.get_current_user import get_current_user

router = APIRouter()


@router.get(
    "/",
)
def get_todos(
    skip: int = 0,
    limit: int = 10,
    filter_by: str | None = None,
    value: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return todo_crud.get_all_by_user_id(db, user.id, skip, limit, filter_by, value)


@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return todo_crud.get_by_id(db, todo_id, user.id)


@router.post("/")
def create_todo(
    todo: CreateTodo,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> JSONResponse:
    created = todo_crud.create_todo(db, todo, user.id)
    if created:
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Todo created successfully!"},
        )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": "Todo creation failed!"},
    )


@router.put("/{todo_id}")
def update_todo(
    todo_id: int,
    todo: UpdateTodo,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    updated = todo_crud.update_todo(db, todo_id, todo, user_id=user.id)
    if updated:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": "Todo updated"}
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"message": "Todo updation failed"}
    )


@router.delete("/{todo_id}")
def delete_todo(
    todo_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> JSONResponse:
    deleted = todo_crud.delete_todo(db, todo_id, user.id)
    if deleted:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": "Todo deleted"}
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"message": "Todo deletion failed"}
    )
