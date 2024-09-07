from typing import Any, Generic, List, Type, TypeVar

from sqlalchemy.orm import Session

from database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BasicCrud(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db_session: Session):
        self.model_class = model
        self.session = db_session

    def get_by(self, field: str, value: Any) -> ModelType | None:
        return (
            self.session.query(self.model_class)
            .filter(getattr(self.model_class, field) == value)
            .one_or_none()
        )

    def get_all(self, skip: int = 0, limit: int = 10) -> List[ModelType] | None:
        return self.session.query(self.model_class).offset(skip).limit(limit).all()

    def create(self, attributes: dict[str, Any] = None) -> ModelType:
        if attributes is None:
            attributes = {}
        model = self.model_class(**attributes)
        self.session.add(model)
        self.session.commit()
        return True

    def update(self, model: ModelType, attributes: dict[str, Any] = None) -> ModelType:
        if attributes is None:
            return

        for key, value in attributes.items():
            if value:
                setattr(model, key, value)
        self.session.commit()
        return model

    def delete(self, model: ModelType) -> None:
        self.session.delete(model)
        self.session.commit()
