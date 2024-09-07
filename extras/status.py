from enum import Enum


class Status(Enum):
    DONE: str = "done"
    IN_PROGRESS: str = "in_progress"
    TODO: str = "todo"
