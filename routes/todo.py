from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud import todo as todo_crud
from database import get_db
from schemas.todos import CreateTodo, TodoResponse, UpdateTodo

router = APIRouter()


@router.get("/", response_model=List[TodoResponse])
def get_todos(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return todo_crud.get_all(db, skip, limit)


@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db),
):
    return todo_crud.get_by_id(db, todo_id)


@router.post("/")
def create_todo(todo: CreateTodo, db: Session = Depends(get_db)):
    return todo_crud.create_todo(db, todo)


@router.put("/{todo_id}")
def update_todo(todo_id: int, todo: UpdateTodo, db: Session = Depends(get_db)):
    return todo_crud.update_todo(db, todo_id, todo)


@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    return todo_crud.delete_todo(db, todo_id)
