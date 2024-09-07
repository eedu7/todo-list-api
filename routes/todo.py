from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud import todo as todo_crud
from database import get_db
from schemas.todos import CreateTodo, TodoResponse

router = APIRouter()


@router.get("/", response_model=List[TodoResponse])
def get_todos(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 10
) -> List[TodoResponse]:
    return todo_crud.get_all(db, skip, limit)


@router.post("/")
def create_todo(todo: CreateTodo, db: Session = Depends(get_db)):
    return todo_crud.create_todo(db, todo)
