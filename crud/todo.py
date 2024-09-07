from sqlalchemy.orm import Session

from crud import BasicCrud
from models import Todo
from schemas.todos import CreateTodo


def get_all(db: Session, skip: int = 0, limit: int = 10):
    base_crud = BasicCrud(model=Todo, db_session=db)
    return base_crud.get_all(skip, limit)


def create_todo(db: Session, todo: CreateTodo):
    base_crud = BasicCrud(model=Todo, db_session=db)
    created = base_crud.create(todo.model_dump())
    return created
