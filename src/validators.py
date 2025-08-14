from src.enums import Status, PriorityLevel
from src.exceptions import TaskValidationError
from datetime import datetime


def parse_title(title) -> str:
    if not isinstance(title, str):
        raise TaskValidationError('Title must be a string')
    if title.strip() == '':
        raise TaskValidationError('Title cannot be empty')
    if len(title) > 255:
        raise TaskValidationError('Title max length is 255 characters')
    return title

def parse_description(description) -> str:
    if not isinstance(description, str):
        raise TaskValidationError('Description must be a string')
    if len(description) > 1000:
        raise TaskValidationError('Description max length is 1000 characters')
    return description

def parse_due_date(due_date) -> str:
    if not isinstance(due_date, str):
        raise TaskValidationError('Due date must be a string in YYYY-MM-DD format')
    if due_date.strip() == '':
        raise TaskValidationError('Due date cannot be empty')
    try:
        dt = datetime.strptime(due_date, '%Y-%m-%d')
    except ValueError as e:
        raise TaskValidationError('due_date must be in YYYY-MM-DD format') from e
    return dt.strftime('%Y-%m-%d')

def parse_priority(priority: str | PriorityLevel) -> PriorityLevel:
    """
      'Low', 'low', 'LOW' -> PriorityLevel.LOW
      'Medium', 'MEDIUM' -> PriorityLevel.MEDIUM
      'High', 'HIGH' -> PriorityLevel.HIGH
    """

    if isinstance(priority, PriorityLevel):
        return priority
    if not isinstance(priority, str):
        raise TaskValidationError('Priority must be a string or PriorityLevel enum member')
    raw = priority.strip()
    if not raw:
        raise TaskValidationError('Priority cannot be empty')

    # Try by enum value (case-insensitive)
    for p in PriorityLevel:
        if p.value.lower() == raw.lower():
            return p

    allowed = ', '.join(p.value for p in PriorityLevel)
    raise TaskValidationError(f'Priority must be one of: {allowed}')

def parse_status(status: str | Status) -> Status:
    """
      'Pending', 'pending', 'PENDING' -> Status.PENDING
      'in progress', 'In PrOgreSs' -> Status.IN_PROGRESS
      'completed', 'COMPLETED' -> Status.COMPLETED
    """

    if isinstance(status, Status):
        return status
    if not isinstance(status, str):
        raise TaskValidationError('status must be a string or Status enum member')
    raw = status.strip()
    if not raw:
        raise TaskValidationError('status cannot be empty')
    
    for s in Status:
        if s.value.lower() == raw.replace(' ', '_').lower():
            return s

    allowed = ', '.join(s.value for s in Status)
    raise TaskValidationError(f'status must be one of: {allowed}')

def parse_sorting(sorting: str) -> str:
    if sorting.upper() not in ['ASC', 'DESC']:
        raise TaskValidationError("Sorting must be 'ASC' or 'DESC'")
    return sorting