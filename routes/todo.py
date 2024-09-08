from fastapi import APIRouter, Depends
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
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return todo_crud.get_all_by_user_id(db, user.id, skip, limit)


@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return todo_crud.get_by_id(db, todo_id)


@router.post("/")
def create_todo(
    todo: CreateTodo,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return todo_crud.create_todo(db, todo)


@router.put("/{todo_id}")
def update_todo(
    todo_id: int,
    todo: UpdateTodo,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return todo_crud.update_todo(db, todo_id, todo, user_id=user.id)


@router.delete("/{todo_id}")
def delete_todo(
    todo_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    return todo_crud.delete_todo(db, todo_id, user.id)
