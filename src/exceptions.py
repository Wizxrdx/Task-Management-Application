class DatabaseConnectionError(Exception):
    pass

class DatabaseQueryError(Exception):
    pass

class TaskValidationError(ValueError):
    pass