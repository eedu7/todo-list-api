from typing import Any, Generic, Type, TypeVar

from sqlalchemy.orm import Session

from database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BasicCrud(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db_session: Session):
        self.model_class = model
        self.session = db_session

    def get_by_id(self): ...

    def get_by(self): ...

    def get_all(self, skip: int = 0, limit: int = 10):
        return self.session.query(self.model_class).offset(skip).limit(limit).all()

    def create(self, attributes: dict[str, Any] = None) -> ModelType:
        if attributes is None:
            attributes = {}
        model = self.model_class(**attributes)
        self.session.add(model)
        self.session.commit()
        return model

    def update(self): ...

    def delete(self): ...
