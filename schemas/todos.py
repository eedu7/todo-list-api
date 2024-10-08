from datetime import datetime

from pydantic import BaseModel, Field

from extras import Status


class Base(BaseModel):
    title: str = Field(..., examples=["Buy groceries"])
    description: str = Field(..., examples=["Buy milk, eggs, and bread"])
    status: Status = Field(..., examples=[Status.TODO])


class CreateTodo(Base):
    pass


class UpdateTodo(BaseModel):
    title: str | None = Field(None, examples=["Buy groceries"])
    description: str | None = Field(None, examples=["Buy groceries"])
    status: Status | None = Field(None, examples=[Status.TODO])


class TodoResponse(Base):
    id: int = Field(..., examples=[1, 2])
    created_at: datetime = Field(..., examples=[datetime.now().isoformat()])
    updated_at: datetime | None = Field(None, examples=[datetime.now().isoformat()])
