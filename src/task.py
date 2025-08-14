from datetime import datetime
from src.enums import Status, PriorityLevel
from src.exceptions import TaskValidationError
from src.validators import (
    parse_description,
    parse_due_date,
    parse_title,
    parse_priority,
    parse_status
)


class Task:
    """
    - title: non-empty (after stripping) and <= 255 chars
    - due_date: valid YYYY-MM-DD string
    - priority: one of PriorityLevel
    - status: a Status enum member
    - creation timestamp: ISO-like string (YYYY-MM-DD HH:MM:SS) or datetime passed in
    """
    def __init__(
        self,
        title: str,
        description: str,
        due_date: str,
        priority: str | PriorityLevel,
        status: Status = Status.PENDING,
        idx: int | None = None,
    ):
        self._id = idx
        self._status = status
        self._title = title
        self._description = description
        self._due_date = due_date
        self._priority = priority

    def __str__(self):
        return (
            f'Task(id={self._id}, title={self._title!r}, due_date={self._due_date}, '
            f'priority={self._priority.name}, status={self._status.name})'
        )

    @property
    def id(self):
        return self._id

    @id.setter
    def set_id(self, new_id: int):
        if self._id is not None and self._id != new_id:
            raise TaskValidationError('Task id already set; cannot change.')
        self._id = new_id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value: str):
        self._title = parse_title(value)

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = parse_description(value)

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, value: str):
        self._due_date = parse_due_date(value)

    @property
    def priority(self):
        return self._priority.value

    @priority.setter
    def priority(self, value: str | PriorityLevel):
        self._priority = parse_priority(value)

    @property
    def status(self):
        return self._status.value

    @status.setter
    def status(self, value: Status):
        self._status = parse_status(value)

    def mark_completed(self):
        if self._status is Status.COMPLETED:
            return
        self._status = Status.COMPLETED