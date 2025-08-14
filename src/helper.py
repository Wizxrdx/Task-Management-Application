from typing import Callable, TypeVar
from src.exceptions import TaskValidationError

T = TypeVar('T')


def get_input(message, data_parser: Callable[[str], T] = str, allow_empty: bool = False) -> T:
    data = None
    while data is None:
        try:
            raw = input(message + ' Use CTRL + C to cancel.\n')
            if allow_empty and raw.strip() == '':
                return None  # type: ignore
            data = data_parser(raw)
        except ValueError as e:
            print(f'Input only type of {data_parser.__name__}')
            continue
        except TaskValidationError as e:
            print(f'Input validation failed: {e}')
            continue
        except (KeyboardInterrupt):
            raise KeyboardInterrupt('Input cancelled by user.')
    return data
