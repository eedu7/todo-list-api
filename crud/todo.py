from sqlalchemy.orm import Session

from crud import BasicCrud
from models import Todo
from schemas.todos import CreateTodo, UpdateTodo


def get_all(db: Session, skip: int = 0, limit: int = 10):
    base_crud = BasicCrud(model=Todo, db_session=db)
    return base_crud.get_all(skip, limit)


def get_by_id(db: Session, todo_id: int):
    base_crud = BasicCrud(model=Todo, db_session=db)
    return base_crud.get_by("id", todo_id)


def get_by_user_id(db: Session, user_id: int):
    base_crud = BasicCrud(model=Todo, db_session=db)
    return base_crud.get_by("user_id", user_id)


def create_todo(db: Session, todo: CreateTodo):
    base_crud = BasicCrud(model=Todo, db_session=db)
    created = base_crud.create(todo.model_dump())
    return created


def update_todo(db: Session, todo_id: int, todo: UpdateTodo):
    base_crud = BasicCrud(model=Todo, db_session=db)
    model = get_by_id(db, todo_id)
    if not model:
        return False
    updated = base_crud.update(model, attributes=todo.model_dump())

    if updated:
        return True
    return False


def delete_todo(db: Session, todo_id: int):
    base_crud = BasicCrud(model=Todo, db_session=db)
    model = get_by_id(db, todo_id)
    if not model:
        return False

    base_crud.delete(model)

    return True
