from datetime import datetime

from sqlalchemy import String, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from extras import Status


class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String)
    status: Mapped[Status] = mapped_column(Enum(Status), default=Status.TODO)
    user_id: Mapped[Integer] = mapped_column(Integer, ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=datetime.now)
