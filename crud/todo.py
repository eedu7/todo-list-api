from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from crud import BasicCrud
from models import Todo
from schemas.todos import CreateTodo, UpdateTodo


def get_all(db: Session, skip: int = 0, limit: int = 10):
    base_crud = BasicCrud(model=Todo, db_session=db)
    return base_crud.get_all(skip, limit)


def get_all_by_user_id(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    filter_by: str | None = None,
    value: str | None = None,
):
    base_crud = BasicCrud(model=Todo, db_session=db)

    if filter_by and value:
        todos = base_crud.filter_by(
            field=filter_by, value=value, limit=limit, skip=skip, user_id=user_id
        )
        return todos

    return base_crud.search_by_user_id(user_id, skip, limit)


def get_by_id(db: Session, todo_id: int, user_id: int):
    base_crud = BasicCrud(model=Todo, db_session=db)
    todo = base_crud.get_by("id", todo_id)
    if todo.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized"
        )
    return todo


def get_by_user_id(db: Session, user_id: int):
    base_crud = BasicCrud(model=Todo, db_session=db)
    return base_crud.get_by("user_id", user_id)


def create_todo(db: Session, todo: CreateTodo, user_id: int):
    base_crud = BasicCrud(model=Todo, db_session=db)
    todos = todo.model_dump()
    todos["user_id"] = user_id
    created = base_crud.create(todos)
    return created


def update_todo(db: Session, todo_id: int, todo: UpdateTodo, user_id: int):
    base_crud = BasicCrud(model=Todo, db_session=db)
    model = get_by_id(db, todo_id, user_id)
    if model.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    if not model:
        return False
    updated = base_crud.update(model, attributes=todo.model_dump())

    if updated:
        return True
    return False


def delete_todo(db: Session, todo_id: int, user_id: int):
    base_crud = BasicCrud(model=Todo, db_session=db)
    model = get_by_id(db, todo_id, user_id)
    if model.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    if not model:
        return False

    base_crud.delete(model)

    return True
