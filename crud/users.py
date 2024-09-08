from sqlalchemy.orm import Session

from crud import BasicCrud
from models import User
from schemas.users import UserCreate
from utils import password


def get_by_id(db: Session, user_id: int):
    user_crud = BasicCrud(model=User, db_session=db)
    return user_crud.get_by("id", user_id)


def get_by_email(db: Session, email: str) -> User | None:
    user_crud = BasicCrud(model=User, db_session=db)
    return user_crud.get_by("email", email)


def get_all_users(db: Session, skip: int = 0, limit: int = 10):
    user_crud = BasicCrud(model=User, db_session=db)
    return user_crud.get_all(skip, limit)


def register_user(db: Session, user: UserCreate):
    user_crud = BasicCrud(model=User, db_session=db)
    if user_crud.get_by("email", user.email):
        return False
    data = user.model_dump()
    data["password"] = password.hash_password(data["password"])
    user_crud.create(data)
    return True
