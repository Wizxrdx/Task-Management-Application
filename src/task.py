from datetime import datetime
from src.enums import Status, PriorityLevel
from src.exceptions import TaskValidationError


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
        creation: datetime | str,
        status: Status = Status.PENDING,
        idx: int | None = None,
    ):
        self._id = idx
        self._creation_timestamp = self._coerce_creation(creation)
        self._status = self._validate_status(status)
        self._title = title
        self._description = description
        self._due_date = due_date
        self._priority = priority

    def __str__(self):
        return (
            f'Task(id={self._id}, title={self._title!r}, due_date={self._due_date}, '
            f'priority={self._priority_level}, status={self._status.name}, created={self._creation_timestamp})'
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
        if not isinstance(value, str):
            raise TaskValidationError('Title must be a string')
        value = value.strip()
        if not value:
            raise TaskValidationError('Title cannot be empty')
        if len(value) > 255:
            raise TaskValidationError('Title max length is 255 characters')
        self._title = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value: str):
        if value is None:
            value = ""
        if not isinstance(value, str):
            raise TaskValidationError('Description must be a string')
        value = value.strip()
        if len(value) > 1000:
            raise TaskValidationError('Description max length is 1000 characters')
        self._description = value

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, value: str):
        if not isinstance(value, str):
            raise TaskValidationError('due_date must be a string in YYYY-MM-DD format')
        try:
            dt = datetime.strptime(value, '%Y-%m-%d')
        except ValueError as e:
            raise TaskValidationError('due_date must be in YYYY-MM-DD format') from e
        # store canonical ISO date only
        self._due_date = dt.strftime('%Y-%m-%d')

    @property
    def priority(self):
        return self._priority_level

    @priority.setter
    def priority(self, value: str | PriorityLevel):
        if isinstance(value, PriorityLevel):
            self._priority_level = value.value
            return
        if not isinstance(value, str):
            raise TaskValidationError('Priority must be a string or PriorityLevel enum')
        try:
            self._priority_level = PriorityLevel(value).value
        except ValueError as e:
            allowed = ', '.join(p.value for p in PriorityLevel)
            raise TaskValidationError(f'Priority must be one of: {allowed}') from e

    @property
    def status(self):
        return self._status

    def mark_completed(self):
        if self._status is Status.COMPLETED:
            return
        self._status = Status.COMPLETED